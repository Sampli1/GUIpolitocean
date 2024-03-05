# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me> 


# Import Libraries 
from utils import getComponentAdress
from app import app
from flask import render_template


# Define route "/" & "/<name>"
@app.route("/")
def index():
    src = 0
    return render_template('GUI.html')
