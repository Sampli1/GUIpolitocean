from flask import Flask

app = Flask(__name__, template_folder='template')
app.config['TEMPLATES_AUTO_RELOAD'] = True


import modules
