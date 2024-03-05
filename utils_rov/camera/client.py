from joblib import Parallel, delayed
from vidgear.gears import NetGear
import cv2
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Client:
    def __init__(self, addr, port):
        self.address = addr
        self.port = port

    def receive_frames(self):
        client = NetGear(address=self.address, port=self.port, receive_mode=True)

        while True:
            frame = client.recv()
            if frame is None:
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        client.close()

def read_config(filename="client_config.json"):
    _CONF_DIR = "config/"
    conf_path = os.path.join(basedir, os.path.join(_CONF_DIR, filename))
    print(conf_path)
    with open(conf_path, "r") as f:
        data = json.load(f) 

    return data

def generate_frames(num):
    config = read_config()  
    client = Client(config["client"]["address"], config["client"]["port"][num])
    for frame in client.receive_frames():
        yield frame
