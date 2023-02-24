from flask_restful import Resource, fields, marshal_with, reqparse
from ..models.admin import Venue
from ..db import db
from ..validation import NotFoundError, BusinessValidationError

venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "place" : fields.String,
    "capacity" : fields.Integer,
    "description" : fields.String
}

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('location')
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
        capacity = vn_args.get('capacity',None)
        desc = vn_args.get('description',None)

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


        venue = db.session.query(Venue).filter(Venue.name == name).first()

        if venue:
            raise BusinessValidationError(status_code=400,error_code="VN007",error_message="Venue already exists")

        new_venue = Venue(name=name,location=location,capacity=capacity,description=desc)
        db.session.add(new_venue)
        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        pass
    
class VenueListByCityApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,city):
        venues = db.session.query(Venue).filter(Venue.city == city).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this city',status_code=404,error_code="VN008")
        
    def post(self):
        pass