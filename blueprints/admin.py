from flask import Blueprint, render_template,request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from ..models.admin import Venue, Show
from ..models.users import User
from functools import wraps


admin = Blueprint('admin', __name__,url_prefix='/admin')


def admin_login_required(view):
    @wraps(view)
    def wrap(*args, **kwargs):
        if current_user is not None:
            if current_user.is_admin():
                return view(*args,**kwargs)
            else:
                flash('Not a Admin User...')
                redirect(url_for('authn.login'))
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