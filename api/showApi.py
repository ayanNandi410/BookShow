from flask_restful import Resource, fields, marshal_with, reqparse
from ..models.admin import Show
from ..db import db
from ..validation import NotFoundError, BusinessValidationError

show_output_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "ratings" : fields.String,
    "tags" : fields.List
}

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('name')
create_show_parser.add_argument('ratings')
create_show_parser.add_argument('tags')


class ShowAPI(Resource):

    @marshal_with(show_output_fields)
    def get(self,name):
        shows = db.session.query(Show).filter(Show.name == name).first()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='Show not found',status_code=404,error_code="SW001")


    def post(self):
        vn_args = create_show_parser.parse_args()
        name = vn_args.get('name',None)
        tags = vn_args.get('tags',None)
        ratings = vn_args.get('ratings',None)

        if name is None or name is '':
            raise BusinessValidationError(status_code=400,error_code="SW002",error_message="Name is required")
    
        if tags is None:
            raise BusinessValidationError(status_code=400,error_code="SW003",error_message="A Single Tag is required")

        if ratings is None:
            raise BusinessValidationError(status_code=400,error_code="SW004",error_message="Initial rating is required")

        show = db.session.query(Show).filter(Show.name == name).first()

        if show:
            raise BusinessValidationError(status_code=400,error_code="SW007",error_message="Show already exists")

        new_show = Show()
        db.session.add(new_show)
        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        pass
    
class ShowListByVenueApi(Resource):

    @marshal_with(show_output_fields)
    def get(self,venueName):
        shows = db.session.query(Show).filter(venueName in Show.avVenues).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Shows found for this venue',status_code=404,error_code="SW008")
        
    def post(self):
        pass

class ShowListByNameApi(Resource):

    @marshal_with(show_output_fields)
    def get(self,name):
        shows = db.session.query(Show).filter(Show.name.ilike(f'%{name}%')).all()

        if shows:
            return shows
        else:
            raise NotFoundError(error_message='No Venues found for this name',status_code=404,error_code="SW010")
        
    def post(self):
        pass