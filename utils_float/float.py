from serial import Serial, SerialException
import json
import time
import matplotlib.pyplot as plt
import os


def plot_pressure_time(json_files):
    for file_name in json_files:
        with open(file_name, 'r') as file:
            data = json.load(file)
            pressures = data['pressures']
            times = data['times']
            
            plt.plot(times, pressures, label=file_name)
    
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Pressure vs Time')
    plt.legend()
    plt.savefig("mygraph.png")


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
                if (status(s)):
                    return 1
            except SerialException:
                continue
        return 0
    
    

def drop(s:Serial):
    s.write(b'GO')
    s.reset_input_buffer()
    return 1
    

def status(s:Serial):
    timeout = 2 # secondi
    time_i = time.time()
    try:
        s.write(b'STATUS')
        while True:    
            line = s.readline()
            if (line.strip() == b'CONNECTED' or line.strip() == b'IMMERSION'):
                s.reset_input_buffer()
                return 1
            if (time.time() - time_i > timeout):
                return 0
    except SerialException:
        # USB staccata
        s.close()
        return 0

def listen(s: Serial):
    try:
        while True:
            line = s.readline()
            if (line.strip() == b'STOP_DATA'):
                break
            print(line)
        s.close()
        plot_pressure_time([os.path.dirname(os.path.abspath(__file__)) + "/config/data.json"])
    except SerialException:

        # USB staccata
        s.close()
        return 0


