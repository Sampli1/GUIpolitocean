from app import app
import os
from flaskwebgui import FlaskUI


def start_flask(**server_kwargs):
    app = server_kwargs.pop("app", None)
    server_kwargs.pop("debug", None)

    try:
        import waitress

        waitress.serve(app, **server_kwargs)
    except:
        app.run(**server_kwargs)


if __name__ == "__main__":
    FlaskUI(
        server=start_flask,
        server_kwargs={
            "app": app,
            "port": 3000,
            "threaded": True,
        },
        fullscreen= True,
    ).run()
    # app.run("0.0.0.0", port=os.getenv('PORT', 6969), debug=True)


