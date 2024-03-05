import os
import string

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPONENTS_PATH = os.path.join(APP_PATH, 'components/')

def getComponentAdress(comp: str) -> str:
    return os.path.join(COMPONENTS_PATH, f"{comp}.html")