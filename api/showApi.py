from flask_restful import Resource, fields, marshal_with, reqparse, inputs
import json
from models.admin import Show, Venue, Tag, Language
from sqlalchemy import select,join
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
            raise BusinessValidationError(status_code=400,error_code="SW005",error_message="Invalid value for rating")

        if duration is None:
            raise BusinessValidationError(status_code=400,error_code="SW006",error_message="Duration is required")


        show = db.session.query(Show).filter(Show.name == name).first()

        if show:
            raise BusinessValidationError(status_code=400,error_code="SW011",error_message="Show already exists")

        from datetime import datetime
        timestamp = datetime.now()

        new_show = Show(name=name,rating=rating,duration=duration,timestamp=timestamp)
        for tagName in tags:
            tag = db.session.query(Tag).filter(Tag.name == tagName).first()
            new_show.tags.append(tag)
        for langName in languages:
            lng = db.session.query(Language).filter(Language.name == langName).first()
            new_show.languages.append(lng)
        #new_show.tags.append()

        #vid = db.session.query(Venue.id).filter(Venue.name == venue).first()
        #allocation = DayAllocation(venue_id=vid,show_id=new_show.id,date=rlDate,timeslot=rlTime,price=ticketPrice)
        db.session.add(new_show)
        print("Show added :",new_show.tags,new_show.languages)
        #db.session.add(allocation)

        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        pass
    
class ListShowByVenueApi(Resource):

    @marshal_with(userShow_output_fields)
    def get(self,venue):
        venue = db.session.query(Venue).filter(Venue.name == venue).first()
        shows = venue.shows
        
        if len(shows) == 0:
            raise NotFoundError(error_message='No Shows found for this venue',status_code=404,error_code="SW0013")
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
            raise NotFoundError(error_message='No Venues found for this name',status_code=404,error_code="SW014")
        
    def post(self):
        pass