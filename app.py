from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__, template_folder='template')
app.config['TEMPLATES_AUTO_RELOAD'] = True


cors = CORS(app)
socketio = SocketIO(app, engineio_logger = True, logger=True, debug=True,cors_allowed_origins='*', cors_credentials=False,async_mode='eventlet')



import modules
