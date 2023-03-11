from flask import Blueprint, request
import requests
from flask import render_template
from flask_login import login_required, current_user
from ..models.admin import Venue, Show
from ..constants import BASE_URL

user = Blueprint('user', __name__,url_prefix='/user')

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
    #venue = Venue.query.filter_by(name = name).first()
    # all shows here
    #print(cur_venue.avShows)

    return render_template('userVenueHome.html',venue=cur_venue, user=current_user)