from flask_restful import Resource, fields, marshal_with, reqparse, inputs
import json
from models.admin import Show, Venue, Allocation
from datetime import date, timedelta
from flask import request
from sqlalchemy import desc
from db import db
from validation import NotFoundError, BusinessValidationError
from datetime import datetime as dt

allocation_output_fields = {
    "date" : fields.String,
    "time" : fields.String,
    "avSeats" : fields.Integer,
    "totSeats" : fields.Integer,
    "price" : fields.Float
}

create_allocation_parser = reqparse.RequestParser()
create_allocation_parser.add_argument('venue_name')
create_allocation_parser.add_argument('show_name')
create_allocation_parser.add_argument('releaseDate')
create_allocation_parser.add_argument('releaseTime')
create_allocation_parser.add_argument('allocSeats',type=int, help="Seats must be an integer")
create_allocation_parser.add_argument('price', type=float, help="Not a valid number or price")



class AllocationAPI(Resource):

    @marshal_with(allocation_output_fields)
    def get(self):
        showName = request.args.get('show')
        venueName = request.args.get('venue')

        show = db.session.query(Show).filter(Show.name == showName).first()
        venue =db.session.query(Venue).filter(Venue.name == venueName).first()

        timeslotList = db.session.query(Allocation.timeslot,Allocation.avSeats,Allocation.totSeats,Allocation.price).filter(Allocation.venue == venue,Allocation.show == show,Allocation.timeslot > date.today(),Allocation.timeslot < (date.today()+timedelta(days=7))).order_by(Allocation.timeslot).all()

        if not timeslotList:
            raise NotFoundError(error_message='No timeslots found',status_code=404,error_code="AL011")
        else:
            slotlist = []
            for row in timeslotList:
                slotDict = { "date" : row.timeslot.strftime("%Y-%m-%d"), "time" : row.timeslot.strftime("%H:%M:%S"), 
                            "avSeats" : row.avSeats, "totSeats" : row.totSeats, "price" : row.price }
                slotlist.append(slotDict)
            print(slotDict)
            return slotlist, 200

    def post(self):
        vn_args = create_allocation_parser.parse_args()
        venueName = vn_args.get('venue_name',None)
        showName = vn_args.get('show_name',None)
        rlDate = vn_args.get('releaseDate',None)
        rlTime = vn_args.get('releaseTime',None)
        allcSeats = vn_args.get('allocSeats',None)
        ticketPrice = vn_args.get('price',None)

        if venueName is None or venueName == '':
            raise BusinessValidationError(status_code=400,error_code="AL001",error_message="Venue Name is required")
    
        if showName is None or showName == '':
            raise BusinessValidationError(status_code=400,error_code="AL002",error_message="Show Name is required")

        if float(ticketPrice) < 0.0:
            raise BusinessValidationError(status_code=400,error_code="AL003",error_message="Invalid value for Ticket Price")

        try:
            rDate = dt.strptime(rlDate, "%d-%m-%Y").date()
        except(ValueError):
            raise BusinessValidationError(status_code=400,error_code="AL004",error_message="Invalid Date or date format")

        try:
            rTime = dt.strptime(rlTime, "%H:%M:%S").time()
        except(ValueError):
            raise BusinessValidationError(status_code=400,error_code="AL005",error_message="Invalid Time or time format")

        if allcSeats is None:
            raise BusinessValidationError(status_code=400,error_code="AL006",error_message="Allocated seat count is required")

        if int(allcSeats) <= 0:
            raise BusinessValidationError(status_code=400,error_code="AL007",error_message="Invalid seat count")


        show = db.session.query(Show).filter(Show.name == showName).first()

        if not show:
            raise BusinessValidationError(status_code=400,error_code="AL008",error_message="Show does not exist")

        venue = db.session.query(Venue).filter(Venue.name == venueName).first()

        if not venue:
            raise BusinessValidationError(status_code=400,error_code="AL009",error_message="Venue does not exist")

        from datetime import datetime
        timestamp = datetime.now()

        timeslot = datetime.combine(rDate,rTime)

        show_id = db.session.query(Show.id).filter(Show.name == showName).first()
        venue_id = db.session.query(Venue.id).filter(Venue.name == venueName).first()

        new_allocation = Allocation(show_id=show_id.id,venue_id=venue_id.id,timeslot=timeslot,totSeats=allcSeats,avSeats=allcSeats,price=ticketPrice)
        
        db.session.add(new_allocation)

        db.session.commit()
        return "Success", 201

    def put(self,name):
        pass
    
    def delete(self,name):
        pass