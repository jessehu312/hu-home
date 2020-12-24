from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
from datetime import datetime

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')

app = Flask(__name__, template_folder=TEMPLATE_PATH)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
  socketio.run(app)

@app.route('/')
def client():
  return render_template('client.html')

@socketio.on('update')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('roster', {'time': str(datetime.now().isoformat()), 'members': [{'clientId': 123}]})