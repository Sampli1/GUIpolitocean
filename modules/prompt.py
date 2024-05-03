import os
from app import app
from flask import request
import paramiko
from dotenv import load_dotenv
import threading 

load_dotenv()

# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

# # Dizionario per mantenere traccia delle connessioni SSH per ogni client
# ssh_sessions = {}
# def run_ssh_command(client, command):
    # stdin, stdout, stderr = client.exec_command(command)
    # output = stdout.read().decode()
    # return output

# # Funzione per l'apertura di una sessione SSH utilizzando Paramiko
# def open_ssh_session():
    # hostname = os.getenv('SSH_HOSTNAME')
    # port = int(os.getenv('SSH_PORT'))
    # username = os.getenv('SSH_USERNAME')
    # password = os.getenv('SSH_PASSWORD')
    # try:
        # client.connect(hostname, port=port, username=username, password=password, timeout=3)
        # print("[SSH] CONNECTED")
    # except TimeoutError:
        # print("[SSH] FAILED")


# # Funzione di gestione per l'apertura di una sessione SSH
# @socketio.on('SSH_connection')
# def ssh_connection(json):
    # print("[SSH] Connection ...")
    # threading.Thread(target=open_ssh_session).start()

# # Funzione di gestione per i comandi SSH inviati dal client
# @socketio.on('SSH_command')
# def ssh_command(json):
    # data = json['cmd']
    # sid = request.sid
    # if client.get_transport() is not None:
        # if client.get_transport().is_active():
            # output = run_ssh_command(client, data)
            # socketio.emit('SSH_OUTPUT', output)
    # else:
        # socketio.emit('SSH_OUTPUT', 'Sessione SSH non aperta. Connetti prima alla sessione SSH.')
