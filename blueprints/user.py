from flask import Blueprint
import requests
from flask import render_template
from flask_login import login_required, current_user
from ..models.admin import Venue, Show
from ..constants import BASE_URL

user = Blueprint('user', __name__,url_prefix='/user')


@user.route('/userProfile')
@login_required
def userProfile():
    return render_template("userProfile.html", user=current_user)

@user.route('/venues')
@login_required
def userVenues():
    venues = Venue.query.all()
    return render_template('userVenues.html',venues=venues, user=current_user)

@user.route('/venueHome/<name>')
@login_required
def userVenueHome(name):
    venueCall = requests.get(BASE_URL+'/api/venue/'+name)
    venue = venueCall.json()

    #venue = Venue.query.filter_by(name = name).first()
    # all shows here
    shows = Show.query.all()

    return render_template('userVenueHome.html',venue=venue,shows=shows, user=current_user)