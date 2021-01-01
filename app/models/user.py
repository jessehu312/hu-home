from app.database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    firebase_id = db.Column(db.Integer(), nullable=True)

    def __init__(self, username, firebase_id):
        self.email = username
        self.firebase_id = firebase_id

    def __repr__(self):
        return "<User: {}>".format(self.username)
