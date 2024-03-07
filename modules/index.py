# Import Libraries 
from utils import getComponentAdress
from app import app
from flask import render_template, redirect


@app.route("/")
def main():
    return render_template('GUI.html')

# Define route "/" & "/<name>"
@app.route("/ROV")
def gui():
    return render_template("ROV.html")

@app.route("/flaskwebgui-keep-server-alive", methods=["GET"])
def responde():
    return '{"content": "mammt"}'
