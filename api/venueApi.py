from flask_restful import Resource, fields, marshal_with, reqparse
from models.admin import Venue, Allocation
from db import db
from validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc

venue_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "location" : fields.String,
    "city" : fields.String,
    "capacity" : fields.Integer,
    "description" : fields.String,
    "timestamp" : fields.DateTime(dt_format='rfc822')

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
         

        if name is None or name == '':
            raise BusinessValidationError(status_code=400,error_code="VN002",error_message="Name is required")
    
        if location is None or location == '':
            raise BusinessValidationError(status_code=400,error_code="VN003",error_message="Location is required")

        if city is None or city == '':
            raise BusinessValidationError(status_code=400,error_code="VN004",error_message="City is required")

        if capacity == None or type(capacity) is not int:
            raise BusinessValidationError(status_code=400,error_code="VN005",error_message="Invalid capacity of venue")
        
        if int(capacity) < 40:
            raise BusinessValidationError(status_code=400,error_code="VN006",error_message="Capacity must be atleast 40")
        
        if desc is None or desc == '':
            raise BusinessValidationError(status_code=400,error_code="VN007",error_message="Description is required")


        venue = db.session.query(Venue).filter(Venue.name == name).first()

        if venue:
            raise BusinessValidationError(status_code=400,error_code="VN008",error_message="Venue already exists")

        from datetime import datetime
        timestamp = datetime.now()

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
        showForVenue = db.session.query(Allocation).filter(Allocation.venue_id == venue.id).first()

        if showForVenue:
            raise BusinessValidationError(status_code=400,error_code="VN012",error_message="Venue has shows allocated to it")

        db.session.delete(venue)
        db.session.commit()
        return "Success", 200

    
class VenueListByCityApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,city):
        venues = db.session.query(Venue).filter(Venue.city == city).order_by(desc(Venue.timestamp)).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this city',status_code=404,error_code="VN009")
        
    def post(self):
        pass

class VenueListByNameApi(Resource):

    @marshal_with(venue_output_fields)
    def get(self,name):
        venues = db.session.query(Venue).filter(Venue.name.ilike(f'%{name}%')).order_by(desc(Venue.timestamp)).all()

        if venues:
            return venues
        else:
            raise NotFoundError(error_message='No Venues found for this name',status_code=404,error_code="VN010")
        
    def post(self):
        pass

# entities = MyEntity.query.order_by(desc(MyEntity.time)).limit(3).all()