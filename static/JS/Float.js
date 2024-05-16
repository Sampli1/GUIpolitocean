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
    const drop = document.getElementsByClassName("status DROP");
    const immersion = document.getElementsByClassName("status IMMERSION")[0];
    if (!status.status) status = await startFloat();
    console.log(status);
    sts = status.text.split("|");
    for (let i = 0; i < sts.length; i++) {
        switch (sts[i].trim()) {
            case "CONNECTED":
                serial.classList.add("on");
                ready.classList.remove("on");                
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                break;

            case "CONNECTED&READY":
                serial.classList.add("on");
                ready.classList.add("on");                
                for (let i = 0; i < drop.length; i++) drop[i].classList.add("enabled");

                break;
            case "IMMERSION":
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                
                immersion.classList.add("immersion");
                break;
            case "FINISHED":
                immersion.classList.remove("immersion");
                for (let i = 0; i < drop.length; i++) drop[i].classList.add("enabled");
                publishReport(status);
                break;
            case "DATA_ABORTED":
                
                break
            case "NO USB":
                console.warn("USB ESP-B NOT FOUND");
                serial.classList.remove("on");
                ready.classList.remove("on");
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");

        }
    }
}

let msgs = ["GO", "SEND_DATA_ABORT", "SWITCH_AUTO_MODE", "DATA_ABORT", "TRY_UPLOAD"]

async function msg(e, msg_id) {
    const data = await fetch(`FLOAT/msg?msg=${msgs[msg_id]}`);
    if (data.status == 201) {
        //
    }
    else {
        alert("Is USB cable connected?")
    }
}
