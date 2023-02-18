from ..db import db

class Image(db.Model):
    id = db.Column(db.String(50), primary_key=True, autoincrement=True)
    data = db.Column(db.String())
    name = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "<Image File : "+self.name