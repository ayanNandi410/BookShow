from flask_restful import Resource, fields, marshal_with
from flask import request, jsonify
from flask_login import current_user
from datetime import date, timedelta
from models.admin import BookTicket
from db import db
from validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc

venue_output_fields = {
    "name" : fields.String
}

venue_output_fields = {
    "name" : fields.String
}

booking_output_fields = {
    "venue" : fields.Nested(venue_output_fields),
    "show" : fields.Nested(),
    "date" : fields.String,
    "timeslot" : fields.String,
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

class BookTicketAPI(Resource):

    @marshal_with(booking_output_fields)
    def get(self):
        email = current_user.email

        bookings = db.session.query(BookTicket).filter(BookTicket.user_email == email).order_by(BookTicket.timestamp.desc()).all()

        if not bookings:
            raise NotFoundError(error_message='No timeslot found',status_code=404,error_code="TS001")
        else:
            return bookings, 200


    def post(self):
        pass

    def put(self,name):
        pass
    
    def delete(self,name):
        pass