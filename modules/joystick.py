from app import app
from flask import Response, render_template, jsonify, make_response
from utils_rov.controller.controller import ROVController

contr = ROVController()
print(contr.status())
@app.route('/controller')
def controller_status():
    contr.run()
    pass
