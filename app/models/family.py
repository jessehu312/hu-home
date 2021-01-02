from app.database import db
from uuid import uuid4

cols = ('name', 'address', 'city', 'zip', 'phone', 'geofence_id')

class Family(db.Model):
    __tablename__ = 'family'

    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    zip = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=True)
    geofence_id = db.Column(db.String(80), nullable=True)

    def __init__(self, args):
        self.id = str(uuid4())

        for key in cols:
          if key in args:
            setattr(self, key, args[key])

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def to_dict(self):
        d = {}
        for k in cols:
            val = getattr(self, k)
            if val:
                d[k] = val
        return d
