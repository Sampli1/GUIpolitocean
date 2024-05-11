from app import app
from flask import jsonify, request, make_response

@app.route("/PID/set", methods = ['POST'])
def setData():
    rq = request.form
    print(rq)
    return make_response(jsonify(rq), 200)  