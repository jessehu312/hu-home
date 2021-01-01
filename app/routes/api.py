from flask import Blueprint, request
from app import settings
from firebase_admin import auth
from app.models.user import User
from app.database import db

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/client-config')
def client_config():
    return settings.FIREBASE_CLIENT_CONFIG

def list_users():
    return list(map(lambda row: {'id': row.id, 'username': row.email, 'firebase_id': row.firebase_id}, User.query.all()))

def add_user(id, email):
    if not User.query.filter_by(firebase_id=id).first():
        user = User(username = email, firebase_id = id)
        db.session.add(user)
        db.session.commit()
    return list_users()

@blueprint.route('/get-user', methods=['POST'])
def get_user():
    id_token = request.json.get('token')
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    email = decoded_token['email']
    decoded_token['listUsers'] = add_user(uid, email)
    return decoded_token, 200
