from joblib import Parallel, delayed
import os 
import json

from vidgear.gears import CamGear
from vidgear.gears import NetGear
import cv2


basedir = os.path.abspath(os.path.dirname(__file__))

class Camera:
    def __init__(self, addr, port, camera_id, camera_config):
        self.address = addr
        self.port = port
        self.camera = camera_id
        self.camera_config = camera_config
    
    def send_stream(self):
        stream = CamGear(source=self.camera, **self.camera_config).start()
        server = NetGear(address=self.address, port=self.port)
        
        try:
            while True:
                frame = stream.read()

                if frame is None:
                    break

                server.send(frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        except Exception as e:
            print(e)
        
        finally:
            server.close()
            stream.stop()


def read_config(filename="server_config.json"):
    _CONF_DIR = "config/" 
    conf_path = os.path.join(basedir, os.path.join(_CONF_DIR, filename))
    with open(conf_path, "r") as f:
        data = json.load(f)

    return data

def server_process(num, config):
    camera = Camera(config["server"]["address"], config["server"]["port"][num], 
                    config["camera"][1]["CAMERA_SOURCE"][num], config["camera"][0])
    camera.send_stream()

def joblib_loop(config, nj):
    Parallel(n_jobs=nj)(delayed(server_process)(i, config) for i in range(nj))    

if __name__ == "__main__":
    config = read_config()
    joblib_loop(config, config["num_cameras"])
