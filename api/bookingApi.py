from flask_restful import Resource, fields, marshal_with
from flask import request, jsonify
from flask_login import current_user
from datetime import date, timedelta
from models.admin import BookTicket
from db import db
from validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc

class MyDate(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')
    
class MyTime(fields.Raw):
    def format(self, value):
        return value.strftime('%H-%M-%S')

venue_output_fields = {
    "name" : fields.String
}

show_output_fields = {
    "name" : fields.String
}

alloc_output_fields = {
    "date" : MyDate,
    "timeslot" : MyTime,
    "price" : fields.String
}

booking_output_fields = {
    "venue" : fields.Nested(venue_output_fields),
    "show" : fields.Nested(show_output_fields),
    "allocation": fields.Nested(alloc_output_fields),
    "totPrice" : fields.String,
    "allocSeats" : fields.Integer,
    "timestamp" : fields.DateTime(dt_format='rfc822')
}

class BookTicketAPI(Resource):

    @marshal_with(booking_output_fields)
    def get(self,email):

        bookings = db.session.query(BookTicket).filter(BookTicket.user_email == email).order_by(BookTicket.timestamp.desc()).all()

        if not bookings:
            raise NotFoundError(error_message='No Booking found',status_code=404,error_code="BK001")
        else:
            return bookings, 200


    def post(self):
        pass

    def put(self,name):
        pass
    
    def delete(self,name):
        pass