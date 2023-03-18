from flask import Blueprint, request
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
    venues = Venue.query.all()

    return render_template('userVenues.html',venues=venues, user=current_user)

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
    

@user.route('/bookTimeslot/')
@login_required
def bookTimeslot():
    show = request.args.get('show')
    venue = request.args.get('venue')

    query = {'show': show, 'venue': venue}
    timeslotsCall = requests.get(BASE_URL+'/api/getTimeslots',params=query)
    timeslots = timeslotsCall.json()

    slots = {}

    for item in timeslots:
        if item['date'] in slots.keys() :
            if item['avSeats'] == 0:
                slots[item['date']].append((item['timeslot'],item['avSeats'],item['price']))
            else:
                slots[item['date']].append((item['timeslot'],item['avSeats'],item['price']))
        else:
            slots[item['date']] = []
            if item['avSeats'] == 0:
                slots[item['date']].append((item['timeslot'],item['avSeats'],item['price']))
            else:
                slots[item['date']].append((item['timeslot'],item['avSeats'],item['price']))

    print(slots)

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

    print(slots)
    print(dayList)

    return render_template("bookTimeslot.html", dayList=dayList,show=show,venue=venue,slotsDict=slots, user=current_user)


@user.route('/bookTicket/')
@login_required
def bookTicket():
    show = request.args.get('show')
    venue = request.args.get('venue') 
    date = request.args.get('date')
    time = request.args.get('time')
    price = request.args.get('price')

    details = { "show": show, "venue": venue, "date": date, "time": time,"price": float(price), "email": current_user.email}

    return render_template('bookTicket.html',details=details,user=current_user)

@user.route('/bookings/')
@login_required
def showBookings():
    return render_template('userBookings.html',user=current_user)