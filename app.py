from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='template')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# TODO
# socketio = SocketIO(app, debug=True, cors_allowed_origins='*',async_mode='eventlet')



import modules
