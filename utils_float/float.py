from serial import Serial, SerialException
import json
import time
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64


def plot_pressure_time(data):
    pressures = data['pressures']
    times = data['times']         
    plt.plot(times, pressures, label='ciao.png')
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Pressure vs Time')
    plt.legend()
    plt.grid()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return base64_img
    
def start_communication(s: Serial):
    if (s.is_open):
        return 1
    with open(os.path.dirname(os.path.abspath(__file__)) +"/config/float.json") as jmaps:
        conf = json.load(jmaps)
        s.baudrate = conf['baudrate']
        for i in range(0, 4):
            dir = f"{conf['port']}{i}"
            try:
                s.port = dir
                s.open()
                if (status(s)['status']):
                    return 1
            except SerialException:
                continue
        return 0
     

def status(s:Serial):
    timeout = 2 # secondi
    time_i = time.time()
    try:
        s.write(b'STATUS\n')
        while True:    
            line = s.readline().strip()
            if (line == b'CONNECTED' or line == b'IMMERSION' or line == b'CONNECTED READY'):
                return {
                    'text': line.strip().decode(),
                    'status': 1
                }
            elif (line == b'UPLOAD_DATA'):
                # Lettura dati

                times = []
                pressures = []
                while (True):                    
                    line = s.readline().strip()
                    if (line == b'STOP_DATA'):
                        break
                    data = json.loads(line.decode())
                    times.append(data['times'])
                    pressures.append(data['pressures'])


                json_complete = {
                    "times": times,
                    "pressures": pressures
                }   
                data = plot_pressure_time(json_complete)
                return {
                    'text': "FINISHED",
                    'status': 1,
                    'data': data,
                }

            if (time.time() - time_i > timeout):
                return {
                    'text': "DISCONNECTED",
                    'status': 0
                }

    except SerialException:
        # USB staccata
        s.close()
        return {
            'text': "DISCONNECTED",
            'status': 0
        }


def drop(s: Serial):
    s.reset_output_buffer()
    s.write(b'GO\n')
