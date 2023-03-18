from flask_restful import Resource, fields, marshal_with, reqparse
from ..models.admin import Venue
from ..db import db
from ..validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc

venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "location" : fields.String,
    "city" : fields.String,
    "capacity" : fields.Integer,
    "description" : fields.String,
    "timestamp" : fields.String

}

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('location')
create_venue_parser.add_argument('city')
create_venue_parser.add_argument('capacity',type=int, help='Capacity cannot be converted')
create_venue_parser.add_argument('description')

class VenueAPI(Resource):

    @marshal_with(venue_output_fields)
    def get(self,name):
        venues = db.session.query(Venue).filter(Venue.name == name).first()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='Venue not found',status_code=404,error_code="VN001")


    def post(self):
        vn_args = create_venue_parser.parse_args()
        name = vn_args.get('name',None)
        location = vn_args.get('location',None)
        city = vn_args.get('city',None)
        capacity = vn_args.get('capacity',None)
        desc = vn_args.get('description',None)
        from datetime import datetime
        timestamp = datetime.now()
         

        if name is None or name is '':
            raise BusinessValidationError(status_code=400,error_code="VN002",error_message="Name is required")
    
        if location is None or location is '':
            raise BusinessValidationError(status_code=400,error_code="VN003",error_message="Location is required")

        if capacity is None or capacity is '':
            raise BusinessValidationError(status_code=400,error_code="VN004",error_message="Capacity is required")

        if int(capacity) <40:
            raise BusinessValidationError(status_code=400,error_code="VN005",error_message="Invalid capacity of venue")
        
        if desc is None or desc is '':
            raise BusinessValidationError(status_code=400,error_code="VN006",error_message="Description is required")
    
        if city is None or city is '':
            raise BusinessValidationError(status_code=400,error_code="VN007",error_message="City is required")
    


        venue = db.session.query(Venue).filter(Venue.name == name).first()

        if venue:
            raise BusinessValidationError(status_code=400,error_code="VN007",error_message="Venue already exists")

        new_venue = Venue(name=name,location=location,city=city,capacity=int(capacity),description=desc,timestamp=timestamp)
        db.session.add(new_venue)
        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        venue = db.session.query(Venue).filter(Venue.name == name).first()

        if not venue:
            raise BusinessValidationError(status_code=400,error_code="VN011",error_message="Venue not found with such name")
        
        # check for dependency

        db.session.delete(venue)
        db.session.commit()
        return "Succesfully Deleted", 200

    
class VenueListByCityApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,city):
        venues = db.session.query(Venue).filter(Venue.city == city).order_by(desc(Venue.timestamp)).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this city',status_code=404,error_code="VN008")
        
    def post(self):
        pass

class VenueListByNameApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,name):
        venues = db.session.query(Venue).filter(Venue.name.ilike(f'%{name}%')).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this name',status_code=404,error_code="VN010")
        
    def post(self):
        pass

# entities = MyEntity.query.order_by(desc(MyEntity.time)).limit(3).all()