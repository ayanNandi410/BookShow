from flask import Flask, render_template
from flask_login import LoginManager
from .blueprints.authentication import authn as userAuth
from .blueprints.admin import admin as adminProfile
from .blueprints.user import user as userProfile
from .models.users import User
from .init_api import getConfiguredApi
from .testData import generateTestData
from .db import db

def create_app():
    app = Flask(__name__)

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
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('NotFound.html',errorMessage=e), 404

    generateTestData(app,db)

    api = getConfiguredApi(app)
    return app, api