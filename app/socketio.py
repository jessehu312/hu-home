import os
from flask_socketio import SocketIO, emit
from datetime import datetime

STALE_CLIENT_THRESHOLD = 30 # seconds

def init_socketio(app):
  socketio = SocketIO(app)
  register_handlers(socketio)
  return socketio

def register_handlers(socketio):
  clients = {}

  @socketio.on('update')
  def handle_my_custom_event(json):
      print('received json: ' + str(json))
      json['timestamp'] = int(datetime.now().timestamp())
      clients[json['clientId']] = json
      cleanup_clients()
      emit('roster', {'time': str(datetime.now().isoformat()), 'members': list(clients.values())})

  def cleanup_clients():
    stale_clients = []
    current_time = datetime.now().timestamp()
    for key,value in clients.items():
      if int(current_time - STALE_CLIENT_THRESHOLD) > value['timestamp']:
        stale_clients.append(key)
    for client in stale_clients:
      clients.pop(client)