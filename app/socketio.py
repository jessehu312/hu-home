import os
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from datetime import datetime

STALE_CLIENT_THRESHOLD = 30 # seconds

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