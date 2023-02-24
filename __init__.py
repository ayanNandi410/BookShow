from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager
from .blueprints.authentication import authn as userAuth
from .blueprints.admin import admin as adminProfile
from .blueprints.user import user as userProfile
from werkzeug.security import generate_password_hash
from .models.users import User
from .models.admin import Show,Tag,Venue,tags
from .db import db

def create_app():
    app = Flask(__name__)
    apiV = Api(app)

    UPLOAD_FOLDER = '/uploads/'

    app.config['SECRET_KEY'] = 'ABCD12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketdb.sqlite'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # blueprint for authentication routes
    app.register_blueprint(userAuth)

    # blueprint for admin routes
    app.register_blueprint(adminProfile)

    # blueprint for user routes
    app.register_blueprint(userProfile)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authn.userLogin'
    login_manager.login_message = "You need to login first!!"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

       #db.drop_all()
        #db.create_all()

    #@app.before_first_request
    #def create_admin():
    #    db.session.add(User(name='admin',email='admin@gmail.com',password=generate_password_hash('admin123', method='sha256'),access=1))
    #    db.session.commit()

    with app.app_context():
        db.drop_all()
        db.create_all()

        inoxHighland = Venue(name='Inox Highland Park',description='Again 1 of the Topmost Multiplex in Kolkata. As I am a Movie Buff, watching 4-5 Movies in a month, there is hardly any Good Multiplex or Cinema Hall in Central Kolkata and nearby, where I haven`t been.',location='Dharmatala',city='Kolkata',capacity=320)
        inoxRangoli = Venue(name='Inox Rangoli Mall',description='Again 1 of the Topmost Multiplex in Kolkata. As I am a Movie Buff, watching 4-5 Movies in a month, there is hardly any Good Multiplex or Cinema Hall in Central Kolkata and nearby, where I haven`t been.',location='Belur',city='Howrah',capacity=540)
        inoxForum = Venue(name='Inox Forum Mall',description='Again 1 of the Topmost Multiplex in Kolkata. As I am a Movie Buff, watching 4-5 Movies in a month, there is hardly any Good Multiplex or Cinema Hall in Central Kolkata and nearby, where I haven`t been.',location='Rabindra Sadan',city='Kolkata',capacity=340)
        inoxRD = Venue(name='Inox RD Mall',description='Again 1 of the Topmost Multiplex in Kolkata. As I am a Movie Buff, watching 4-5 Movies in a month, there is hardly any Good Multiplex or Cinema Hall in Central Kolkata and nearby, where I haven`t been.',location='Liluah',city='Howrah',capacity=200)

        db.session.add_all([inoxRangoli,inoxForum,inoxHighland,inoxRD])

        db.session.add(User(name='admin',email='admin@gmail.com',password=generate_password_hash('admin123', method='sha256'),access=1))
        db.session.commit()

    # Api initialization
    from .api.venueApi import VenueAPI, VenueListByCityApi
    apiV.add_resource(VenueAPI,"/api/venue","/api/venue/<string:name>",endpoint="/venue")
    apiV.add_resource(VenueListByCityApi,"/api/venues/<string:city>",endpoint="/venues/<city>")
    return app, apiV