/*
statuses: [index -> meaning]
0 -> SERIAL CONNECTED
1 -> FLOAT READY TO DEPLOY
2 -> FLOAT IN IMMERSION
*/

let statuses = [0, 0, 0];
let nReport = 1;

async function startFloat() {
    let response = await fetch("/FLOAT/start");
    let status = await response.json();
    return status;
}

function publishReport(data) {
    const tab = document.getElementsByClassName("g1")[0];
    let img = document.createElement('img');
    let div = document.createElement('div');
    let p = document.createElement('p');
    p.innerText = `REPORT #${nReport++}`;
    div.classList.add('report');
    img.src = "data:image/jpeg;charset=utf-8;base64," + data.data;
    div.append(p);
    div.append(img);
    tab.appendChild(div);
}

async function statusFLOAT() {
    let response = await fetch("/FLOAT/status");
    let status = await response.json();
    const serial = document.getElementsByClassName("status SERIAL")[0];
    const ready = document.getElementsByClassName("status READY")[0];
    const drop = document.getElementsByClassName("status DROP")[0];
    const immersion = document.getElementsByClassName("status IMMERSION")[0];
    if (!status.status) status = await startFloat();
    console.log(status)
    switch (status.code) {
        case "CONNECTED":
            serial.classList.add("on");
            break;
        case "CONNECTED READY":
            serial.classList.add("on");
            ready.classList.add("on");
            drop.classList.add("enabled");
            drop.classList.remove("disabled");
            break;
        case "IMMERSION":
            drop.classList.remove("enabled");
            immersion.classList.add("immersion");
            break;
        case "FINISHED":
            immersion.classList.remove("immersion");
            drop.classList.toggle("on");
            publishReport(status);
            break;
        case "NO USB":
            console.warn("USB ESP-B NOT FOUND");
    }
}



async function drop(e) {
    if (statuses.every((x) => x == 1)) return;
    const data = await fetch("FLOAT/drop");
    if (data.status == 201) {
        dropped = 1;
        e.classList.toggle("on");
    }
    else {
        alert("Is USB cable connected?")
    }
}