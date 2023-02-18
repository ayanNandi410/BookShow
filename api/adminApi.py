from flask_restful import Resource, fields, marshal_with, reqparse
from ..models.admin import Venue
from ..db import db
from ..validation import NotFoundError, BusinessValidationError

venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "place" : fields.String,
    "capacity" : fields.Integer
}

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('place')
create_venue_parser.add_argument('capacity',type=int, help='Capacity cannot be converted')

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
        name = vn_args.get("name",None)
        place = vn_args.get("place",None)
        capacity = vn_args.get("capacity",None)

        if name is None:
            raise BusinessValidationError(status_code=400,error_code="VN002",error_message="name is required")
    
        if place is None:
            raise BusinessValidationError(status_code=400,error_code="VN003",error_message="place is required")

        if capacity is None:
            raise BusinessValidationError(status_code=400,error_code="VN004",error_message="capacity is required")

        if int(capacity) <40:
            raise BusinessValidationError(status_code=400,error_code="VN005",error_message="Invalid capacity of venue")

        venue = db.session.query(Venue).filter(Venue.name == name).first()

        if venue:
            raise BusinessValidationError(status_code=400,error_code="VN006",error_message="Venue already exists")

        new_venue = Venue(name=name,place=place,capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        pass
    