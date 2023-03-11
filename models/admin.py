from ..db import db
from sqlalchemy.sql import func

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

languages = db.Table('languages',
    db.Column('lang_id', db.Integer, db.ForeignKey('Language.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    location = db.Column(db.String(30))
    city = db.Column(db.String(30))
    capacity = db.Column(db.Integer)
    timestamp = db.Column(db.String(20))

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
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return "< Show : "+self.name+">"

class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class Language(db.Model):
    __tablename__ = 'Language'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lname = db.Column(db.String(20), nullable=False)

class DayAllocation(db.Model):
    __tablename__ = 'Day Allocation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer)
    show_id = db.Column(db.Integer)
    day = db.Column(db.String(10))
    timeslot = db.Column(db.String(10))
    price = db.Column('Ticket_Price',db.Numeric(10,2))