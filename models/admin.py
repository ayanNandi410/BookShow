from db import db
from sqlalchemy.sql import func
from datetime import datetime

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

languages = db.Table('languages',
    db.Column('lang_id', db.Integer, db.ForeignKey('Language.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class Language(db.Model):
    __tablename__ = 'Language'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    location = db.Column(db.String(30))
    city = db.Column(db.String(30))
    capacity = db.Column(db.Integer)
    shows = db.relationship('Show',secondary='Allocation',lazy='subquery', viewonly=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return "< Venue : "+self.name+">"

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    rating = db.Column(db.Integer)
    duration = db.Column(db.String(20))
    languages = db.relationship('Language', secondary=languages, lazy='subquery',
        backref=db.backref('show', lazy=True))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('show', lazy=True))
    venues = db.relationship('Venue',secondary='Allocation',lazy='subquery', viewonly=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return "< Show : "+self.name+">"

class Allocation(db.Model):
    __tablename__ = 'Allocation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('Show.id'), nullable=False)
    timeslot = db.Column(db.DateTime(timezone=True), nullable=False) # contains both date and time of show
    totSeats = db.Column('Total Seats',db.Integer,nullable=False)
    avSeats =db.Column('Available Seats',db.Integer,nullable=False)
    price = db.Column('Ticket Price',db.Numeric(10,2), nullable=False)

    bookings = db.relationship('BookTicket', backref='allocShow',lazy=True)
    venue = db.relationship('Venue')
    show = db.relationship('Show')
    #venue = db.relationship('Venue', backref= db.backref('DayAllocation', cascade='all, delete-orphan' ))
    #show = db.relationship('Show', backref= db.backref('DayAllocation', cascade='all, delete-orphan' ))

    def __repr__(self):
        return "< Allocation : "+self.venue.name+","+self.show.name+","+str(self.timeslot)+","+str(self.date)+">"

class BookTicket(db.Model):
    __tablename__ = 'BookTicket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    showAllocId = db.Column(db.Integer,db.ForeignKey('Allocation.id'),nullable=False)
    user_email = db.Column(db.String(40),nullable=False)
    allocSeats = db.Column('Seats Booked',db.Integer,nullable=False)
    totPrice = db.Column('Total Price',db.Numeric(12,2))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    allocation =  db.relationship('Allocation',lazy='subquery', viewonly=True)
    venue = db.relationship('Venue',secondary='Allocation',lazy='subquery', viewonly=True)
    show = db.relationship('Show',secondary='Allocation',lazy='subquery', viewonly=True)