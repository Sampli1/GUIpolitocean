from vidgear.gears import CamGear
from vidgear.gears import NetGear
import cv2


class Camera:
    def __init__(self, addr, port, camera_id, camera_config):
        self.address = addr
        self.port = port
        self.camera = camera_id
        self.camera_config = camera_config
    
    def send_stream(self):
        stream = CamGear(source=self.camera, **self.camera_config).start()
        server = NetGear(address=self.address, port=self.port)

        while True:
            frame = stream.read()

            if frame is None:
                break

            server.send(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            
        server.close()
        stream.stop()

