from flask import Blueprint, render_template,request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from datetime import datetime
from ..models.admin import Venue, Show
from ..models.users import User
#from ..models.Image import Image
from functools import wraps
from werkzeug.utils import secure_filename
from ..db import db
import requests
from ..constants import BASE_URL

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

admin = Blueprint('admin', __name__,url_prefix='/admin')


def admin_login_required(view):
    @wraps(view)
    def wrap(*args, **kwargs):
        if current_user is not None:
            if current_user.is_admin():
                return view(*args,**kwargs)
            else:
                flash('Not a Admin User...')
                redirect(url_for('authn.userLogin'))
        else:
            flash('You need to login first.')
            return redirect(url_for('authn.adminLogin'))
    return wrap

@admin.route('/')
@admin_login_required
def index():
    return render_template('adminHome.html',user=current_user)


@admin.route('/profile')
@admin_login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@admin.route('/showVenues')
@admin_login_required
def showVenues():
    page = request.args.get('page', 1, type=int)
    paginationVenue = Venue.query.order_by(Venue.name).paginate(page=page, per_page=20)
    return render_template('venuesHome.html',pagination=paginationVenue, user=current_user)

@admin.route('/showVenues/<city>')
@admin_login_required
def showVenuesByCity(city):
    venues = requests.get(BASE_URL+'/api/venues/'+city)
    return render_template('venuesHome.html',venues = venues,city=city, user=current_user)

@admin.route('/deleteVenue/<name>')
@admin_login_required
def deleteVenue(name):
    delVenueCall = requests.delete(BASE_URL+'/api/venue/'+name)
    response = delVenueCall.json()
    print(response)
    return redirect(url_for('admin.showVenues'))

# -------------------- Shows ---------------------

@admin.route('/showShows')
@admin_login_required
def showShows():
    page = request.args.get('page', 1, type=int)
    paginationShow = Show.query.order_by(Show.timestamp).paginate(page=page, per_page=20)
    return render_template('showsHome.html',pagination=paginationShow, user=current_user)

@admin.route('/venue/add',methods=['GET','POST'])
@admin_login_required
def addVenue():
    if request.method == 'POST':
        name = request.form.get('venueName')
        location = request.form.get('venueLocation')
        city = request.form.get('venueCity')
        description = request.form.get('venueDescription')
        capacity = request.form.get('venueCapacity')
        venue = { 'name' : name, 'location' : location, 'city' : city, 'description' : description, 
        'capacity' : capacity }

        resV = requests.post(BASE_URL+'/api/venue', json=venue)
        
        return render_template('addVenue.html',response=resV.json(), user=current_user)
    else:
        return render_template('addVenue.html', user=current_user)
    
@admin.route('/showFor/<vname>/add',methods=['GET','POST'])
@admin_login_required
def addShow(vname):
    if request.method == 'POST':
        name = request.form.get('showName')
        venue = request.form.get('venueName')
        tags = request.form.getlist('tags')
        languages = request.form.getlist('languages')
        rating = request.form.get('showRating')
        rlDate = request.form.get('showReleaseDate')
        rlTime = request.form.get('showReleaseTime')
        duration = request.form.get('showDuration')
        ticketPrice = request.form.get('showTicketPrice',type=float)

        showWithAllocation = { 'name' : name, 'vname' : venue, 'tags' : tags, 'languages' : languages,
                 'rating' : int(rating), 'releaseDate' : rlDate, 'releaseTime' : rlTime, 'duration' : duration,
                  'price' : ticketPrice }
        print(showWithAllocation)

        resS = requests.post(BASE_URL+'/api/show', json=showWithAllocation)
        
        return render_template('addShow.html',venue_name=vname,response=resS.json(),user=current_user), 201
    else:

        return render_template('addShow.html',venue_name=vname,user=current_user)