import subprocess
from app import app

@app.route("/promp/<command>")
def cmd(command):
    return subprocess.check_output(command)