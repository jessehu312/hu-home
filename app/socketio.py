import os
from flask import request, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from datetime import datetime
from app.services.radar import radar_client
from threading import Timer

STALE_CLIENT_THRESHOLD = 30 # seconds
blueprint = Blueprint('update', __name__, url_prefix='/update')

def init_socketio(app):
  socketio = SocketIO()
  socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins='*')
  register_handlers(socketio)
  return socketio

def register_handlers(socketio):
  families = {}
  clients = {}

  @socketio.on('connect')
  def handle_connect():
    user_id = request.headers.get('x-client-id')
    family_id = request.headers.get('x-family-id')
    
    if family_id not in families:
      families[family_id] = {user_id}
    else:
      families[family_id].add(user_id)
    join_room(family_id)

  @socketio.on('disconnect')
  def handle_disconnect():
    user_id = request.headers.get('x-client-id')
    family_id = request.headers.get('x-family-id')

    families[family_id].remove(user_id)
    if family_id in families and not families[family_id]:
      families.pop(family_id)
      close_room(family_id)

    clients.pop(user_id)
    leave_room(family_id)

  @socketio.on('update')
  def handle_my_custom_event(json):
    user_id = request.headers.get('x-client-id')
    family_id = request.headers.get('x-family-id')

    json['timestamp'] = int(datetime.now().timestamp())
    clients[user_id] = json
    # cleanup_clients()
    send_roster(family_id)

  def send_roster(family_id):    
    emit('roster', {
      'id': family_id,
      'time': str(datetime.now().isoformat()), 
      'members': {uid: clients.get(uid) for uid in families.get(family_id)}
    }, room=family_id)

  def cleanup_clients():
    stale_clients = []
    current_time = datetime.now().timestamp()
    for key,value in clients.items():
      if int(current_time - STALE_CLIENT_THRESHOLD) > value['timestamp']:
        stale_clients.append(key)
    for client in stale_clients:
      clients.pop(client)

  def remove_client(user_id, family_id):
    families[family_id].remove(user_id)
    if family_id in families and not families[family_id]:
      families.pop(family_id)

    clients.pop(user_id)

  @blueprint.route('/event', methods=['POST'])
  def track():
    try:
      payload = request.json['event']
      if 'user_id' in payload['user']:
        user_id = payload['user']['userId']
      else:
        user = radar_client.users.get(payload['user']['_id'])
        user_id = user['userId']

      family_id = Users.query.get(user_id).family_id
      clients[user_id] = payload
      if family_id not in families:
        families[family_id] = {user_id}
      else:
        families[family_id].add(user_id)
      send_roster(family_id)
      
      t = Timer(10.0, remove_client, args=[user_id, family_id])
    except Exception as e:
      print(e)

    return 'OK', 200
      