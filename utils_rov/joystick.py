import json
import time
import os
import sdl2
import sdl2.ext

__COMMAND_CONFIG_FILE__ = "joystick_Move.yaml"

MIN_AXIS = -32768

class Joystick():
    def __init__(self, commands, on_axis_changed, on_button_changed):
        self.__commands = commands
        self.__on_axis_changed = on_axis_changed
        self.__on_button_changed = on_button_changed
        self.__axesStates = {
                                "X" : 0,
                                "Y": 0,
                                "Z_UP": MIN_AXIS,
                                "Z_DOWN": MIN_AXIS
                                }
        self.active = False
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        sdl2.SDL_GameControllerAddMappingsFromFile("ciao.txt".encode())
        self.__path_mappings = os.path.join(os.path.dirname(__file__), "config/XboxOneController.json")

    @property
    def axesStates(self):
        return self.__axesStates

    @property
    def name(self):
        return sdl2.SDL_JoystickName(self.__joystick).decode("utf-8")

    @property
    def commands(self):
        return self.__commands

    @property
    def mappings(self):
        return self.__mappings
    
    def __open(self):
        self.__joystick = sdl2.SDL_JoystickOpen(0)
        print("[...] Loading mappings")
        print(self.name)
        with open(self.__path_mappings, "r") as jmaps:
            mappings = json.load(jmaps)

            if self.name in mappings:
                self.__mappings = mappings[self.name]
        self.active = True

    def __close(self):
        sdl2.SDL_JoystickClose(self.__joystick)
        self.active = False

    def update(self):
        for event in sdl2.ext.get_events():
            print(event)
            """ 
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.signals.axisChanged.emit(QJoystickAxis(
                    self.__mapping['axes'][event.jaxis.axis], event.jaxis.value))
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.signals.buttonChanged.emit(QJoystickButton(
                    self.__mapping['buttons'][event.jbutton.button], event.jbutton.state))
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.signals.buttonChanged.emit(QJoystickButton(
                    self.__mapping['buttons'][event.jbutton.button], event.jbutton.state))
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.__open()
                print("[+] Joystick added")
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.__close()
                print("[+] Joystick removed")
            """
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.__on_axis_changed(self.__mappings["axes"][event.jaxis.axis], event.jaxis.value)
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.__open()
                print("[JOYSTICK] Joystick added")
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.__close()
                print("[JOYSTICK] Joystick removed")
            elif event.type == sdl2.SDL_JOYBUTTONDOWN or event.type == sdl2.SDL_JOYBUTTONUP:
                self.__on_button_changed(self.__mappings["buttons"][event.jbutton.button], event.jbutton.state)

            #time.sleep(0.03)
            sdl2.ext.get_events().clear()


    def status(self):
        return self.active
