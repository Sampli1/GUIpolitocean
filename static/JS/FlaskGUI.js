let info;
let script = document.currentScript;
let fullUrl = script.src;
let jsonUrl = fullUrl.replace("JS/FlaskGUI.js", "info.json");
let STATUS = {
    "CONTROLLER": 0,
    "SERIAL":0
};
let pages = ["ROV", "FLOAT"];



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

function statusController() {
    
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

    loadPages("ROV");
    loadPages("FLOAT");

    page_now = "home";
    


    // CALL ESSENTIAL FOR ROV

    // controller.run()


    // start with ROV:


    let refresh = 2000;
    setInterval(statusFLOAT, refresh);
    setInterval(statusController, refresh);
    setInterval(keep_alive_server, interval_request);
})
