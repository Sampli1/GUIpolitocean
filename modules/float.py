from app import app
from flask import Response, render_template


@app.route('/FLOAT')
def float():
    return render_template("FLOAT.html")
