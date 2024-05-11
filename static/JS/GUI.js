let info;
let script = document.currentScript;
let fullUrl = script.src;
let jsonUrl = fullUrl.replace("JS/GUI.js", "info.json");
let pages = ["ROV", "FLOAT", "PID"];


// [UTILS]
async function getRequest(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        cache: 'no-cache',
        headers: {
            'Accept': 'application/json',
        },
    })
    return response.json()
}

async function postRequest(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Accept': 'application/json',
        },
        body: JSON.stringify(data)
    })
    return response.json()
}



// Need this to prevent closing of server
function keep_alive_server() {
    let route = "/flaskwebgui-keep-server-alive"
    getRequest(route);
}


// [PAGES]
async function loadPages(page) {
    page_now = pages[page];
    const newpage = await (await fetch(page)).text();
    let parser = new DOMParser();
    let html = parser.parseFromString(newpage, "text/html");
    let wh = document.querySelectorAll(".window")[0];
    wh.append(html.body.firstChild);
}

// [CONTROLLER]
async function statusController() {
    let response = await fetch("/CONTROLLER/start_status");
    let status = await response.json();
    const joystick = document.getElementsByClassName("status CONTROLLER")[0];
    console.log(status);
    if (status['status']) joystick.classList.add("on")
    else joystick.classList.remove("on");
}

document.addEventListener('DOMContentLoaded', async function () {

    // Force dimensions of window
    let h = window.innerHeight;
    let w = window.innerWidth;
    let body = document.getElementsByTagName('body')[0];
    body.style.width = `${w}px`; 
    body.style.height = `${h}px`;


    console.log(jsonUrl)

    // Load Info
    info = await getRequest(jsonUrl)

    console.log(info)

    // Load pages    
    for (let i = 0; i < pages.length; i++) loadPages(pages[i]);
    page_now = "home";
    


   
    
    // Routines
    let refresh = 2000;
    setInterval(statusFLOAT, refresh);
    setInterval(statusController, refresh);
    setInterval(keep_alive_server, refresh + 1000);
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


