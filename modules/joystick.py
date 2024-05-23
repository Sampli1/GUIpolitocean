from app import app
from flask import jsonify, make_response
from utils_rov.controller import ROVController
import threading

contr = ROVController()

data = {'status': 0, 'isRunning': 0, 'code': 'CONTROLLER'}

@app.route('/CONTROLLER/start_status')
async def controller():
    if (contr.configured and not contr.is_running):
        threading.Thread(target=contr.run).start()

    data['status'] = contr.status()
    data['isRunning'] = contr.is_running
    return make_response(jsonify(data), 201)
