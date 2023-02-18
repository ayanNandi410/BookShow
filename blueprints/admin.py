from flask import Blueprint, render_template,request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from ..models.admin import Venue, Show
from ..models.users import User
from ..models.Image import Image
from functools import wraps
from werkzeug.utils import secure_filename

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
    return 'Index'


@admin.route('/profile')
@admin_login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@admin.route('/showVenues')
@admin_login_required
def showVenues():
    venues = Venue.query.all()
    return render_template('venuesHome.html',venues = venues, user=current_user)

@admin.route('/showShows')
@admin_login_required
def showShows():
    shows = Show.query.all()
    return render_template('showsHome.html',shows=shows, user=current_user)

@admin.route('/venue/add')
@admin_login_required
def addVenue():
    if request.method == 'POST':
        name = request.form.get('venueName')
        location = request.form.get('venueLocation')
        description = request.form.get('venueDescription')
        capacity = request.form.get('venueCapacity')
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('addVenue.html')
        file = request.files['venueImage']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('addVenue.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            img = Image(data=file,name=filename,type=file.mimetype)
            Venue = Venue(name=name,location=location,description=description,capacity=capacity,img_name=filename)

            
            return redirect(url_for('download_file', name=filename))
    else:
        return render_template('addVenue.html')