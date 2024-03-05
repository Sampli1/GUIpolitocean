from app import app
from flask import Response, request
from utils_rov.camera.client import generate_frames


@app.route('/video_feed/<num>', methods=['GET'])
def video_feed(num):
    print(num)
    return Response(generate_frames(int(num)), mimetype='multipart/x-mixed-replace; boundary=frame')


def zoom():
    print("cock")