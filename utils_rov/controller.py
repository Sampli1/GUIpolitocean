import os
import sys
import yaml
import json
from yamlinclude import YamlIncludeConstructor

from .mqtt_c import MQTTClient
from .joystick import Joystick


__CONFIG_FILENAME__ = "config.yaml"
__CONFIG_JOYSTICK_KEY__ = "joystick"
__CONFIG_MQTT_KEY__ = "mqtt"

class ROVController():
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "config")

        self.__configured = False
        self.is_running = False
        
        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader, base_dir=path)

        if not os.path.isdir(path):
            sys.exit("[!] Config path must be a directory")
       
        configFilePath = os.path.join(path, __CONFIG_FILENAME__)
        if not os.path.isfile(configFilePath):
           sys.exit("[!] Config directory must contain config.yaml")

        with open(configFilePath, "r") as yconfig:
            config = yaml.load(yconfig, Loader=yaml.FullLoader)
            
            self.__mqttClient = self.__init_mqttClient(config[__CONFIG_MQTT_KEY__])
            self.__joystick = self.__init_joystick(config[__CONFIG_JOYSTICK_KEY__])

            self.__configured = True

    def __init_joystick(self, config):
        joystick = Joystick(config, self.__on_axisChanged, self.__on_buttonChanged)
        return joystick

    def __init_mqttClient(self, config):
        mqttClient = MQTTClient(config["id"], config["address"], config["port"])
        mqttClient.connect()
         
        return mqttClient
   
    @property
    def configured(self):
        return self.__configured

    def mqttClient(self):
        return self.__mqttClient if self.__configured else None
    
    def joystick(self):
        return self.__joystick if self.__configured else None

    def __on_axisChanged(self, id_axes, value):
        print(id_axes, value)
        self.__joystick.axesStates[self.__joystick.commands['axes'][id_axes]] = value
        print(json.dumps(self.__joystick.axesStates))
        self.__mqttClient.publish('axis/', json.dumps(self.__joystick.axesStates))
    
    def __on_buttonChanged(self, id_button, state):
        if state:
            command = self.__joystick.commands["buttons"][id_button]["onPress"]
        else:
            command = self.__joystick.commands["buttons"][id_button]["onRelease"]

        self.__mqttClient.publish("commands/", command)

    def __on_mqttStatusChanged(self, status):
       pass

    def run(self):
        self.is_running = True
        while True:
            self.__joystick.update()

    def status(self):
        return self.__joystick.active