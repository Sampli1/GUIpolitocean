import subprocess
from app import app
import sys, time
from flask import Response, url_for
from shelljob import proc


g = proc.Group()

@app.route('/prompt/<cmd>')
def prompt(cmd):
    p = g.run( cmd.split() )
    prompt = url_for('static', filename='./CSS/prompt.css')
    def read_process():
        yield f"<link rel='stylesheet' href='{prompt}'>"
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield f"<p class='line'>{line.decode()}</p>"
        yield f"<p class='line stop'>--- STOP</p>"
    return Response(read_process(), mimetype= 'text/html' )

@app.route("/prompt/interrupt")
def stop():
    g.close()
    g.clear_finished()
    
    return "Process interrupted"
