from flask import Blueprint, request
from app import settings
from firebase_admin import auth

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/client-config')
def client_config():
    return { 
        'firebase': settings.FIREBASE_CLIENT_CONFIG,
        'radar': settings.RADAR_PUBLISHABLE_KEY
    }

@blueprint.route('/get-user', methods=['POST'])
def get_user():
    id_token = request.json.get('token')
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    return decoded_token, 200