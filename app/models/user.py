from app.database import db

cols = ('id', 'email', 'name', 'family_id')

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=True)
    family_id = db.Column(db.String(80), nullable=True)

    def __init__(self, username, firebase_id):
        self.email = username
        self.id = firebase_id

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def to_dict(self):
        d = {}
        for k in cols:
            val = getattr(self, k)
            if val:
                d[k] = val
        return d
