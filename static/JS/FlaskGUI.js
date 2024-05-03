let info;
let script = document.currentScript;
let fullUrl = script.src;
let jsonUrl = fullUrl.replace("JS/FlaskGUI.js", "info.json");
let pages = ["ROV", "FLOAT"];
let n_pages = 2;


async function getRequest(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        cache: 'no-cache'
    })
    return response.json()
}

async function loadPages(page) {
    page_now = info.pages[page];
    const newpage = await (await fetch(page)).text();
    let parser = new DOMParser();
    let html = parser.parseFromString(newpage, "text/html");
    let wh = document.querySelectorAll(".window")[0];
    wh.append(html.body.firstChild);
}

async function statusController() {
    let response = await fetch("/CONTROLLER/start_status");
    let status = await response.json();
    const joystick = document.getElementsByClassName("status CONTROLLER")[0];
    console.log(status);
    if (status['status']) joystick.classList.add("on")
    else joystick.classList.remove("on");
}

document.addEventListener('DOMContentLoaded', async function () {
    let route = "/flaskwebgui-keep-server-alive"
    let interval_request = 3 * 1000 //sec
    function keep_alive_server() {
        getRequest(route);
    }


    // Costringi a mantenere le dimensioni
    let h = window.innerHeight;
    let w = window.innerWidth;
    let body = document.getElementsByTagName('body')[0];
    body.style.width = `${w}px`; 
    body.style.height = `${h}px`;
    const data = await fetch(jsonUrl, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    });
    info = await data.json();

    // Load pages    
    for (let i = 0; i < n_pages; i++) loadPages(pages[i]);
    page_now = "home";
    

    // Routines
    let refresh = 2000;
    setInterval(statusFLOAT, refresh);
    setInterval(statusController, refresh);
    setInterval(keep_alive_server, interval_request);
})


// const socket = io("ws://127.0.0.1:5000",{
    // transports: ["websocket"],
    // reconnectionDelayMax: 10000,
// }) 


// socket.on("connect",() => {
    // console.info("[Socket.io] Ready");
    // socket.emit("test", "test");
// });

// socket.on("connect_error", (data) => {
    // console.error("ERROR");
    // console.log(data);
// });
    
// socket.on("disconnect", (reason, details) => {
    // console.info("DISCONNECTED");
    // console.log(reason);
    // console.log(details);
// });

// socket.on('error', (error) => {
    // console.error('ERROR');
    // console.log(error);
// });


