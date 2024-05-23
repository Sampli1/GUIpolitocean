from app import app
from flask import jsonify, request, make_response
import threading
from utils_rov.task2 import fetch_image, STATUS

# ! TASK 2024

THREAD_ACTIVE = False

@app.route('/TASK_2/status')
def task2_status():
    return jsonify(STATUS), 200

@app.route('/TASK_2/start')
def task2_start():
    global THREAD_ACTIVE
    if (not THREAD_ACTIVE):
        threading.Thread(target=fetch_image).start()
        THREAD_ACTIVE = True
        return jsonify({"status": "OK"}), 200
    return jsonify({"error": "Conflict"}), 200

