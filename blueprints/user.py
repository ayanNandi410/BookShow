from flask import Blueprint, request, flash, redirect, url_for
import requests
from datetime import datetime,timedelta
from flask import render_template
from flask_login import login_required, current_user
from models.admin import Venue, Show
from constants import BASE_URL

user = Blueprint('user', __name__,url_prefix='/user')

@user.route('/')
@login_required
def index():
    pass

@user.route('/userHome')
@login_required
def userHome():
    
    cityCall = requests.get(BASE_URL+'/api/city/all')
    cities = cityCall.json()

    return render_template("userHome.html",cities=cities, user=current_user)

@user.route('/userProfile')
@login_required
def userProfile():
    return render_template("userProfile.html", user=current_user)

@user.route('/venues')
@login_required
def userVenues():
    page = request.args.get('page', 1, type=int)
    pagedVenues = Venue.query.order_by(Venue.name).paginate(page=page, per_page=20)

    if pagedVenues.pages == 0:
        return render_template('userVenues.html',venuesPage=pagedVenues,noVenue=True, user=current_user)
    else:
        return render_template('userVenues.html',venuesPage=pagedVenues, user=current_user)

@user.route('/venuesByCity/<city>')
@login_required
def userVenuesByCity(city):
    venueCall = requests.get(BASE_URL+'/api/venues/byCity/'+city)
    venues = venueCall.json()
    return render_template('userVenues.html',venues=venues,city=city, user=current_user)

@user.route('/searchVenueByName',methods=['POST'])
@login_required
def userVenuesByName():
    if request.method == 'POST':
        name = request.form.get('searchVenueName')
        venueCall = requests.get(BASE_URL+'/api/venues/byName/'+name)
        venues = venueCall.json()
        return render_template('userVenues.html',venues=venues,name=name, user=current_user)
    else:
        return render_template('NotFound.html', user=current_user)

@user.route('/venueHome/<name>')
@login_required
def userVenueHome(name):
    venueCall = requests.get(BASE_URL+'/api/venue/'+name)
    venue = venueCall.json()
    venue_id = venue['id']
    cur_venue = Venue.query.filter(Venue.id == venue_id).first()

    showsByVenueCall = requests.get(BASE_URL+'/api/shows/byVenue/'+name)
    shows = showsByVenueCall.json()

    if showsByVenueCall.status_code == 404 and shows['error_code'] == "SW008":
        return render_template('userVenueHome.html',venue=cur_venue,showListEmpty=True, user=current_user)
    else:
        return render_template('userVenueHome.html',venue=cur_venue,shows=shows, user=current_user)
    
# --------------------- Shows -----------------------------

@user.route('/popularShows/', methods=['GET','POST'])
@login_required
def popShows():
    if request.method == 'GET':
        pshowsCall = requests.get(BASE_URL+'/api/popShows/'+current_user.email)
        pshows= pshowsCall.json()
        print(pshows)
        return render_template('userShows.html',shows=pshows,heading="Popular Shows", user=current_user)
    
@user.route('/showsByName/', methods=['GET','POST'])
@login_required
def showsByName():
    if request.method == 'POST':
        name = request.form.get('sname')

        showsByNameCall = requests.get(BASE_URL+'/api/shows/byName/'+name)
        shows = showsByNameCall.json()

        if showsByNameCall.status_code == 404:
            return render_template('userShows.html',heading="Shows with name : "+name,showListEmpty=True, user=current_user)
        else:
            return render_template('userShows.html',shows=shows,heading="Shows with name : "+name, user=current_user)

# ------------------- Timeslot ---------------------------

@user.route('/bookTimeslot/')
@login_required
def bookTimeslot():
    show = request.args.get('show')
    venue = request.args.get('venue')

    query = {'show': show, 'venue': venue}
    timeslotsCall = requests.get(BASE_URL+'/api/allocation',params=query)
    timeslots = timeslotsCall.json()
    print(timeslots)
    slots = {}

    if  timeslotsCall.status_code == 404 and timeslots['error_code'] == "AL011":
        return render_template("bookTimeslot.html",show=show,venue=venue,emptySlotList=True)
    else:
        for item in timeslots:
            if item['date'] in slots.keys() :
                if item['avSeats'] == 0:
                    slots[item['date']].append((item['time'],item['avSeats'],item['price']))
                else:
                    slots[item['date']].append((item['time'],item['avSeats'],item['price']))
            else:
                slots[item['date']] = []
                if item['avSeats'] == 0:
                    slots[item['date']].append((item['time'],item['avSeats'],item['price']))
                else:
                    slots[item['date']].append((item['time'],item['avSeats'],item['price']))

        dateList, dayList = [],[]
        from datetime import date
        curdate = date.today()
        for i in range(7): 
            dateList.append(curdate)
            dayList.append(curdate.strftime("%A"))
            curdate += timedelta(days=1)

        for date in dateList:
            if str(date) not in slots.keys():
                slots[str(date)] = []

        return render_template("bookTimeslot.html", dayList=dayList,show=show,venue=venue,slotsDict=slots, user=current_user)

# ---------------- Ticket Booking ----------------------

@user.route('/bookTicket/', methods=['GET','POST'])
@login_required
def bookTicket():
    show = request.args.get('show')
    venue = request.args.get('venue') 
    date = request.args.get('date')
    time = request.args.get('time')
    price = request.args.get('price')

    details = { "show": show, "venue": venue, "date": date, "time": time,"price": price, "email": current_user.email}

    if request.method == 'GET':
        
        return render_template('bookTicket.html',details=details,user=current_user)
    else:
        show = request.form.get('showName')
        venue = request.form.get('venueName') 
        date = request.form.get('date')
        time = request.form.get('time') 
        seats = request.form.get('allocSeats')
        price = request.form.get('totPrice')

        ticketDetails = { "user_email" : current_user.email,"show_name" : show, "venue_name" : venue, "date" : date, "time" : time, "allocSeats" : int(seats), "totPrice" : price  }

        bookingCall = requests.post(BASE_URL+'/api/booking',json=ticketDetails)
        response = bookingCall.json()

        if bookingCall.status_code != 201:
            if 'error_message' in response.keys():
                flash(response['error_message'],'error')
            else:
                flash('Some error occured. Try Again...','error')
        else:
            flash('Succesfully booked tickets','success') 

        return redirect( url_for('user.userHome') )

@user.route('/bookings/')
@login_required
def showBookings():
    bookingsCall = requests.get(BASE_URL+'/api/booking/'+current_user.email)
    bookings = bookingsCall.json()

    return render_template('userBookings.html',bookings=bookings,user=current_user)

# --------------- Movie Review ---------------------------

@user.route('/review/add', methods=["POST"])
@login_required
def addReview():
    show = request.form.get('showName')
    email = current_user.email
    gRating = request.form.get('userRating')
    comment = request.form.get('userComment')

    reviewJson = { 'show_name' : show, 'user_email' : email, 'rating' : gRating, 'comment' : comment}

    reviewsPostCall = requests.post(BASE_URL+'/api/review',json=reviewJson)
    response = reviewsPostCall.json()

    if reviewsPostCall.status_code != 200:
        if 'error_message' in response.keys():
            flash(response['error_message'],'error')
        else:
            flash('Some error occured. Try Again...','error')
    else:
        flash('Succesfully added your review','success') 

    return redirect(url_for('user.showBookings'))

@user.route('/reviews/<sname>')
@login_required
def getReviews(sname):

    reviewsCall = requests.get(BASE_URL+'/api/review/'+sname)
    reviews = reviewsCall.json()