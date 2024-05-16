from serial import Serial, SerialException
import json
import time
import platform
import matplotlib.pyplot as plt
from datetime import datetime
import os
from io import BytesIO
import base64



def plot_pressure_time(data):
    depth = data['depth']
    time = data['times']    
    plt.plot(time, depth)
    plt.xlabel('Time')
    plt.ylabel('Depth (m)')
    plt.grid()
    plt.gcf().autofmt_xdate()
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
        sys = platform.system()
        dir = f"{conf['port']}"
        for i in range(0, 4):
            try:
                s.port = f"{dir}{i}"
                s.open()
                val = status(s)
                return val
            except SerialException:
                continue
        return {
            'text': "NO USB",
            'status':0
        }
     


def status(s:Serial):
    try:
        s.reset_output_buffer()
        s.write(b'STATUS\n')
        line = s.read_until().strip()
        if (b'UPLOAD_DATA' in line):
            # Lettura dati
            s.reset_input_buffer()
            s.write(b"LISTENING\n")
            times = []
            depth = []
            while (True):
                line_data = s.read_until().strip()
                if (line_data == b'STOP_DATA'):
                    break     
                try:
                    decoded = line_data.decode()
                    print(decoded)
                    float_data = json.loads(decoded)
                    depth.append(float(float_data['depth']))
                    times.append(
                        datetime(int(float_data['year']), int(float_data['month']), int(float_data['day']), int(float_data['hour']), int(float_data["minute"]), int(float_data["second"]))
                    )
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                except KeyError as e:
                    print(f"Missing key in JSON data: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

            json_complete = {
                "times": times,
                "depth": depth 
            }  
            s.write(b"DATA_RECEIVED\n")
            data = plot_pressure_time(json_complete)
            
            return {
                'text': "FINISHED",
                'status': 1,
                'data': data,
            }
        return {
            'text': line.strip().decode(),
            'status': 1
        }
    except SerialException:
        # USB staccata
        s.close()
        return {
            'text': "DISCONNECTED",
            'status': 0
        }
    except TimeoutError:
        # L'esp non risponde
        s.close()
        return {
            'text': "ESP DOESN'T ANSWER",
            'status': 0
        }


def send(s: Serial, msg: str):
    s.reset_output_buffer()
    s.reset_input_buffer()
    s.write(f'{msg}\n'.encode('utf-8'))
