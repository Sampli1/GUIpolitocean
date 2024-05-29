from serial import Serial, SerialException
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime
import os
from io import BytesIO
import base64
import threading


def plot_pressure_time(data):
    depth = data['depth']
    time = data['times']    
    plt.plot(time, depth, linestyle='-', marker='o')
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
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config/float.json") as jmaps:
        conf = json.load(jmaps)
        s.baudrate = conf['baudrate']
        for i in range(0, 5):
            try:
                s.port = f"{conf['port']}{i}"
                s.open()
                val = status(s)
                return val
            except SerialException:
                continue
        return {
            'text': "NO USB",
            'status':0
        }
     

def status(s: Serial):
    try:
        s.write(b'STATUS\n')
        time.sleep(0.03)
        line = s.readline().strip()
        return {
            'text': line.decode(),
            'status': 1
        }

    except SerialException:
        s.close()
        return {
            'text': "DISCONNECTED",
            'status': 0
        }
    except TimeoutError:
        s.close()
        return {
            'text': "ESP DOESN'T ANSWER",
            'status': 0
        }


img_data = {
    'text': "LOADING",
    'status': 1,
    'data': "",
}
thread_active = False


def handle_upload_data(s: Serial):
    global img_data, thread_active
    
    thread_active = True
    
    img_data = {
        'text': "LOADING",
        'status': 1,
        'data': "",
    }
    
    s.write(b"LISTENING\n")
    times = []
    depth = []
    while True:
        line_data = s.readline().strip()
        if line_data == b'STOP_DATA':
            break     
        try:
            decoded = line_data.decode()
            print(decoded)
            
            float_data = json.loads(decoded)
            depth.append(float(float_data['depth']))
            times.append(datetime(
                int(float_data['year']), 
                int(float_data['month']), 
                int(float_data['day']), 
                int(float_data['hour']), 
                int(float_data["minute"]), 
                int(float_data["second"])
            ))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Data error: {e}")
        except (SerialException, TimeoutError):
            break
    
    s.write(b"DATA_RECEIVED\n")
    json_complete = {"times": times, "depth": depth}
    data = plot_pressure_time(json_complete) if times and depth else "NO_DATA"
    img_data = {
        'text': "FINISHED",
        'status': 1,
        'data': data,
    }
    print("THREAD FINISHED")
    thread_active = False



def listen(s: Serial):
    global  thread_active
    if not thread_active and img_data['text'] == "LOADING":
        threading.Thread(target=handle_upload_data, args=(s, )).start()

    return img_data


def reset():
    global img_data
    img_data = {
        'text': "LOADING",
        'status': 1,
        'data': "",
    }

def send(s: Serial, msg: str):
    s.reset_output_buffer()
    s.reset_input_buffer()
    s.write(f'{msg}\n'.encode('utf-8'))
