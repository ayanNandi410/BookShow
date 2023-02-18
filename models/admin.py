from ..db import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

available_shows = db.Table('avShows',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
    )

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    img_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    location = db.Column(db.String(80))
    capacity = db.Column(db.Integer)
    avShows = db.relationship('Show', secondary=available_shows, lazy='subquery',
        backref='avVenues')

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    img_id = db.Column(db.String(50), unique=True)
    rating = db.Column(db.Integer)
    ticketPrice = db.Column(db.Float)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('show', lazy=True))

class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)