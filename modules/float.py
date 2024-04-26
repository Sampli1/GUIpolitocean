from app import app
from flask import jsonify, make_response, request
import serial
from utils_float.float import start_communication, send, status

s = serial.Serial(timeout=2)
data = {'status': "", 'code': "" }

@app.route('/FLOAT/msg')
def float_msg():
    if (not s.is_open):
        data['status'] = False
        data['code'] = "SERIAL NOT OPENED"
        return make_response(jsonify(data), 400)
    msg = request.args.get('msg')
    print(msg)
    send(s, msg=msg)
    data['status'] = True
    data['code'] = 'SUCCESS'
    return make_response(jsonify(data), 201)
    

@app.route('/FLOAT/start')
def float_start():
    status = start_communication(s)
    data = {'status': status['status'], 'code': status['text']}
    return make_response(jsonify(data), 201)


@app.route('/FLOAT/status')
def float_status():
    if (not s.is_open):
        data = {'status': False, 'code': 'SERIAL NOT OPENED'}
        return make_response(jsonify(data), 200)
    sts = status(s)
    if sts['text'] == "FINISHED":   
        data = {'status': sts['status'],
                'code': sts['text'],
                'data': sts['data']
                }
        return make_response(jsonify(data), 201)
    
    data = {'status': sts['status'], 'code': sts['text']}
    return make_response(jsonify(data), 201)

