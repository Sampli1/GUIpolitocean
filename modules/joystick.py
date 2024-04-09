from app import app
from flask import Response, render_template, jsonify, make_response
from utils_rov.controller.controller import ROVController
import asyncio


contr = ROVController()

data = {'status': 0, 'isRunning': 0, 'code': 'CONTROLLER'}

@app.route('/CONTROLLER/status')
def controller_status():
    data['status'] = contr.status()
    data['isRunning'] = contr.is_running
    return make_response(jsonify(data), 201)


@app.route('/CONTROLLER/start')
def controller():
    if (contr.configured and not contr.is_running):
        loop = asyncio.new_event_loop()
        loop.create_task(contr.run())
        loop.run_forever()
    data['isRunning'] = contr.status()
    return make_response(jsonify(data), 201)


# @socketio.on("/SOCKET_CONTROLLER/status")
# def socket_controller_status():
    # # TODO
    # pass