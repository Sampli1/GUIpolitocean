from app import app
from flask import jsonify, make_response, request
import serial
from utils_float.float import start_communication, send, status

s = serial.Serial(timeout=2)

data = {'code': "FLOAT", 'status': 0, 'text': "" }

@app.route('/FLOAT/msg')
def float_msg():
    if (not s.is_open):
        data['status'] = False
        data['text'] = "SERIAL NOT OPENED"
        return make_response(jsonify(data), 400)
    msg = request.args.get('msg')
    send(s, msg=msg)
    data['status'] = True
    data['text'] = 'SUCCESS'
    return make_response(jsonify(data), 201)
    

@app.route('/FLOAT/start')
def float_start():
    status = start_communication(s)
    data['status'] = status['status']
    data['text'] = status['text']
    return make_response(jsonify(data), 201)


@app.route('/FLOAT/status')
def float_status():
    if (not s.is_open):
        data['status'] = False
        data['text'] = 'SERIAL NOT OPENED'
        return make_response(jsonify(data), 200)
    sts = status(s)
    if sts['text'] == "FINISHED":    
        imgdata = {
                'code': data['code'],
                'status': sts['status'],
                'data': sts['data'],
                'text': sts['text']   
            }
        return make_response(jsonify(imgdata), 201)
    
    data['status'] = sts['status']
    data['text'] = sts['text']
    return make_response(jsonify(data), 201)

