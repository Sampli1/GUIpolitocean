from app import app
from flaskwebgui import FlaskUI
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == "__main__":
    # NORMAL
    FlaskUI(
        app=app,
        server="flask",
        fullscreen= True,
        port=5000
    ).run()
    

    # DEBUG SOCKET
    #socketio.run(app,port=5000)
    # SOCKET (Maybe in future will be useful)    
    # FlaskUI(
        # app=app,
        # socketio=socketio,
        # server="flask_socketio",
        # fullscreen= True,
        # port=5000
    # ).run()
