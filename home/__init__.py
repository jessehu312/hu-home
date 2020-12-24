from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
from datetime import datetime

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')

app = Flask(__name__, template_folder=TEMPLATE_PATH)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = {}

if __name__ == '__main__':
  socketio.run(app)

@app.route('/')
def client():
  return render_template('client.html', **{'ip': request.remote_addr})

@socketio.on('update')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    json['timestamp'] = int(datetime.now().timestamp())
    clients[json['clientId']] = json
    #print(clients)
    del_client()
    emit('roster', {'time': str(datetime.now().isoformat()), 'members': list(clients.values())})

def del_client():
  delete_clients = []
  current_time = datetime.now().timestamp()
  for key,value in clients.items():
    print(int(current_time - 10), value['timestamp'])
    if int(current_time - 10) > value['timestamp']:
      delete_clients.append(key)
  for key in delete_clients:
    clients.pop(key)

