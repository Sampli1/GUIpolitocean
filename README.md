# GUI EVA
Developed as a web application using Flask in Python for backend development and HTML, JS, CSS for frontend development. 
## Installation (Linux)
You must have NodeJS and Python
```
python3 -m venv venv
source ./venv/bin/activate
pip install -r 'requirements.txt'
cd ./static
npm install
cd ..
```
Or
```
make install
```
## Installation (Windows)
Good luck
## Usage
```
source ./venv/bin/activate
make test
```
## Roadmap

- [x] General Frontend
- [x] General Backend
- [x] Camera
- [x] Float
- [x] Controller
    - [x] Frontend
    - [x] Backend
    - [x] MQTT connection tests
- [ ] Sensors [ Eventually ]
    - [x] Backend
    - [ ] Frontend
- [x] Migrate from HTTP request to Socket communication [ Optional ]
    - [ ] Controller
    - [ ] Sensors
- [ ] Testing
- [ ] Documentation

## PROBLEMS
* Never tested on Windows

## Documentation
The GUI is developed as a web application where data, such as HTML pages, is fetched via HTTP requests; Real-time information is obtained through WebSocket implementation. Request types are handled by the Flask framework.
![SCHEMA](/static/IMG/SCHEMA.png)
## License
No license
