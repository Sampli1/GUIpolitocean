from app import app
from flask import Response, render_template, jsonify, make_response
import serial
from utils_float.float import start_communication, drop, listen, status


s = serial.Serial()

@app.route('/FLOAT/listen')
def float_listen():
    data = {'status': s.is_open}
    return make_response(jsonify(data), 201)


@app.route('/FLOAT/drop')
def float_go():
    if (not s.is_open):
        data = {'message': 'NO', 'code': 'No'}
        return make_response(jsonify(data), 400)
    drop(s)
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)
    

@app.route('/FLOAT/start')
def float_start():
    status = start_communication(s)
    if (not status):
        data = {'status': status, 'code': 'NO USB'}
        return make_response(jsonify(data), 200)
    data = {'status': status, 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)


@app.route('/FLOAT/status')
def float_status():
    if (not s.is_open):
        data = {'status': False, 'code': 'SERIAL NOT OPENED'}
        return make_response(jsonify(data), 200)
    sts = status(s)

    data = {'status': sts, 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@app.route('/FLOAT')
def float():
    return render_template("FLOAT.html")
