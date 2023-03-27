from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask import request
import json
from models.admin import Show, Venue, Tag, Language, Allocation, BookTicket
from sqlalchemy import select, join, func, exc
from db import db
from validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt

tag_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String
}

language_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String
}

userShow_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "rating" : fields.Integer,
    "duration" : fields.String,
    "tags" : fields.List(fields.Nested(tag_output_fields)),
    "languages" : fields.List(fields.Nested(language_output_fields)),
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

chooseShow_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "duration" : fields.String
}

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('name')
create_show_parser.add_argument('rating',type=int)
create_show_parser.add_argument('tags', type=str, action='append', location='json')
create_show_parser.add_argument('languages', type=str, action='append', location='json')
create_show_parser.add_argument('duration')


class ShowAPI(Resource):

    @marshal_with(userShow_output_fields)
    def get(self,name):
        shows = db.session.query(Show).filter(Show.name == name).first()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='Show not found',status_code=404,error_code="SW001")


    def post(self):
        vn_args = create_show_parser.parse_args()
        name = vn_args.get('name',None)
        tags = vn_args.get('tags',[])
        languages = vn_args.get('languages',[])
        rating = vn_args.get('rating',None)
        duration = vn_args.get('duration',None)

        if name is None or name == '':
            raise BusinessValidationError(status_code=400,error_code="SW002",error_message="Name is required")
    
        if tags is []:
            raise BusinessValidationError(status_code=400,error_code="SW003",error_message="A Single Tag is required")

        if languages is []:
            raise BusinessValidationError(status_code=400,error_code="SW004",error_message="Some Language is required")

        if rating is None:
            raise BusinessValidationError(status_code=400,error_code="SW005",error_message="Initial rating is required")

        if int(rating) < 0 or int(rating) > 10:
            raise BusinessValidationError(status_code=400,error_code="SW006",error_message="Invalid value for rating")

        if duration is None:
            raise BusinessValidationError(status_code=400,error_code="SW007",error_message="Duration is required")


        show = db.session.query(Show).filter(Show.name == name).first()

        if show:
            raise BusinessValidationError(status_code=400,error_code="SW008",error_message="Show already exists")

        tagList = []
        langList = []
        for tagName in tags:
            tag = db.session.query(Tag).filter(Tag.name == tagName).first()
            if not tag:
                raise BusinessValidationError(status_code=400,error_code="SW0021",error_message="Tag "+tagName+" not found")
            tagList.append(tag)

        for langName in languages:
            lng = db.session.query(Language).filter(Language.name == langName).first()
            if not lng:
                raise BusinessValidationError(status_code=400,error_code="SW0022",error_message="Language "+langName+" not found")
            langList.append(lng)

        from datetime import datetime
        timestamp = datetime.now()

        try:
            new_show = Show(name=name,rating=rating,duration=duration,timestamp=timestamp)
            new_show.tags = tagList
            new_show.languages = langList

            db.session.add(new_show)
            db.session.commit()

            return "Success", 201
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="SW017",error_message="Add Transaction failed. Try again")


    def put(self):
        vn_args = create_show_parser.parse_args()
        name = vn_args.get('name',None)
        tags = vn_args.get('tags',[])
        languages = vn_args.get('languages',[])
        rating = vn_args.get('rating',None)
        duration = vn_args.get('duration',None)

        if name is None or name == '':
            raise BusinessValidationError(status_code=400,error_code="SW002",error_message="Name is required")
    
        if tags is []:
            raise BusinessValidationError(status_code=400,error_code="SW003",error_message="A Single Tag is required")

        if languages is []:
            raise BusinessValidationError(status_code=400,error_code="SW004",error_message="Some Language is required")

        if rating is None:
            raise BusinessValidationError(status_code=400,error_code="SW005",error_message="Initial rating is required")

        if int(rating) < 0 or int(rating) > 10:
            raise BusinessValidationError(status_code=400,error_code="SW006",error_message="Invalid value for rating")

        if duration is None:
            raise BusinessValidationError(status_code=400,error_code="SW007",error_message="Duration is required")


        show = db.session.query(Show).filter(Show.name == name).first()

        if not show:
            raise BusinessValidationError(status_code=400,error_code="SW0015",error_message="Show does not exist")

        tagList = []
        langList = []
        for tagName in tags:
            tag = db.session.query(Tag).filter(Tag.name == tagName).first()
            if not tag:
                raise BusinessValidationError(status_code=400,error_code="SW0021",error_message="Tag "+tagName+" not found")
            tagList.append(tag)

        for langName in languages:
            lng = db.session.query(Language).filter(Language.name == langName).first()
            if not lng:
                raise BusinessValidationError(status_code=400,error_code="SW0022",error_message="Language "+langName+" not found")
            langList.append(lng)

        from datetime import datetime
        timestamp = datetime.now()

        try:
            
            show.name = name
            show.rating = int(rating)
            show.duration = duration
            show.tags = tagList
            show.languages = langList
        
            db.session.add(show)
            db.session.commit()

            return "Success", 201
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="SW018",error_message="Update Transaction failed. Try again")

    
    def delete(self,name):
        show = db.session.query(Show).filter(Show.name == name).first()

        if not show:
            raise BusinessValidationError(status_code=400,error_code="SW001",error_message="Show not found with such name")
        
        # check for dependency
        venueForShow = db.session.query(Allocation).filter(Allocation.show == show).first()

        if venueForShow:
            raise BusinessValidationError(status_code=400,error_code="SW008",error_message="Show has been allocated to venues")

        try:
            db.session.delete(show)
            db.session.commit()
            return "Success", 200
        except exc.SQLAlchemyError as e:    # Some Database Error occured
            db.session.rollback()
            raise BusinessValidationError(status_code=500,error_code="VN013",error_message="Delete Transaction failed. Try again")

    
class ListShowByVenueApi(Resource):

    @marshal_with(userShow_output_fields)
    def get(self,venue):
        venue = db.session.query(Venue).filter(Venue.name == venue).first()
        shows = venue.shows
        
        if len(shows) == 0:
            raise NotFoundError(error_message='No Shows found for this venue',status_code=404,error_code="SW009")
        else:
            return shows
        
    def post(self):
        pass

class ListShowByNameApi(Resource):

    @marshal_with(userShow_output_fields)
    def get(self,name):
        shows = db.session.query(Show).filter(Show.name.ilike(f'%{name}%')).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Venues found for this name',status_code=404,error_code="SW010")
        

class ChooseShowApi(Resource):

    @marshal_with(chooseShow_output_fields)
    def get(self):
        query = request.args.get('name')

        shows = db.session.query(Show).filter(Show.name.ilike(f'%{query}%')).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Shows found for this name',status_code=404,error_code="SW011")
        

class PopularShowsApi(Resource):

    @marshal_with(userShow_output_fields)
    def get(self, email):

        popshows = db.session.query(BookTicket.show, func.sum(BookTicket.id).label('bookings')).filter(BookTicket.user_email == email).order_by(func.sum(BookTicket.id)).all()
        print(popshows)
        showids = []
        for row in popshows:
            showids.append(row.id)
        shows = db.session.query(Show).filter(Show.id._in(showids)).limit(10).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Shows found',status_code=404,error_code="SW013")
        