from flask_restful import Resource, fields, marshal_with
from flask import request, jsonify
from datetime import date, timedelta
from models.admin import Venue, Allocation, Show, Venue
from db import db
from validation import NotFoundError, BusinessValidationError
from sqlalchemy import desc

timeslot_output_fields = {
    "date" : fields.String,
    "timeslot" : fields.String,
    "avSeats" : fields.Integer,
    "totSeats" : fields.Integer,
    "price" : fields.Float
}

class TimeSlotAPI(Resource):

    @marshal_with(timeslot_output_fields)
    def get(self):
        showName = request.args.get('show')
        venueName = request.args.get('venue')

        show = db.session.query(Show).filter(Show.name == showName).first()
        venue =db.session.query(Venue).filter(Venue.name == venueName).first()

        slotList = {}

        timeslotList = db.session.query(Allocation.date,Allocation.timeslot,Allocation.avSeats,Allocation.totSeats,Allocation.price).filter(Allocation.venue == venue).filter(Allocation.show == show).filter(Allocation.date > date.today()).filter(Allocation.date < (date.today()+timedelta(days=7))).order_by(Allocation.date,Allocation.timeslot).all()

        if not timeslotList:
            raise NotFoundError(error_message='No timeslot found',status_code=404,error_code="TS001")
        else:
            return timeslotList, 200


    def post(self):
        pass

    def put(self,name):
        pass
    
    def delete(self,name):
        pass