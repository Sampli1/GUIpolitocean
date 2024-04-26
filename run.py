from app import app, socketio
from flaskwebgui import FlaskUI
import logging
# from routines import routines

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



if __name__ == "__main__":
    # DEBUG
    #socketio.run(app,port=5000)

    # loop = asyncio.new_event_loop()
    # loop.create_task(routines())
    # loop.run_forever()

    FlaskUI(
        app=app,
        socketio=socketio,
        server="flask_socketio",
        fullscreen= True,
        port=5000
    ).run()
