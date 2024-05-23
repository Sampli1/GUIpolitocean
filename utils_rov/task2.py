import requests
import time
import os

URL = "http://127.0.0.1:5000/test"
# URL = "http://10.0.0.254:8079/snapshot"
INTERVAL_MS = 1000
SAVE_PATH = os.path.join(os.path.dirname(__file__), "captures")
MAX_IMAGES = 20
STATUS = {
    "status": "STOPPED",
    "data": ""
}

def fetch_image():
    global STATUS

    STATUS["status"] = "STARTED"

    interval_s = INTERVAL_MS / 1000.0  
    
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    STATUS["status"] = "CAPTURING"
    for counter in range(MAX_IMAGES):
        try:
            response = requests.get(URL)
            response.raise_for_status()  

            file_path = os.path.join(SAVE_PATH, f"image_{counter}.jpg")

            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Saved {file_path}")

            time.sleep(interval_s)
        except requests.RequestException as e:
            print(f"Error: {e}")
            time.sleep(interval_s)
    
    STATUS["status"] = "ELABORATING_IMAGES"


    # codice per la finofotocchiogrammetria



    STATUS["status"] = "FINISHED"
    # ? Che risultato in output restituisco in interfaccia?
    STATUS["data"] = "boh"