from ..db import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

allocated_shows = db.Table('avShows',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True),
    db.Column('Ticket_Price',db.Float)
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
    allocShows = db.relationship('Show', secondary=allocated_shows, lazy='subquery',
        backref='avShows')

    def __repr__(self):
        return "< Venue : "+self.name+">"

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    #img_name = db.Column(db.String(50), unique=True)
    rating = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('show', lazy=True))
    entry_date = db.Column(db.String(10))

    def __repr__(self):
        return "< Show : "+self.name+">"

class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

class DayAllocation(db.Model):
    venue_id = db.Column(db.Integer)
    show_id = db.Column(db.Integer)
    day = db.Column(db.String(10), primary_key=True)
    timeslot = db.Column(db.String(10), primary_key=True)
