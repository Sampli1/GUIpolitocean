let nReport = 1;
let mux = 1;
let listening = 0;

async function startFloat() {
    return await getRequest("/FLOAT/start");
}

function publishReport(data) {
    const tab = document.getElementsByClassName("g1")[0];
    let img = document.createElement('img');
    let div = document.createElement('div');
    let p = document.createElement('p');
    p.innerText = `REPORT #${nReport++}`;
    div.classList.add('report');
    if (data.data != "NO_DATA") {
        img.src = "data:image/jpeg;charset=utf-8;base64," + data.data;
        div.append(p);
        div.append(img);
        tab.appendChild(div);
    }
    else {
        div.append(p);
        p.innerText = `NO DATA`;
        tab.appendChild(div);
    }
}

async function listeningFLOAT() {
    const immersion = document.getElementsByClassName("status IMMERSION")[0];
    const listen = document.getElementsByClassName("status LISTENING")[0];
    sts = await getRequest("/FLOAT/listen");
    if (sts["text"] != "LOADING") {
        publishReport(sts);
        listening = 0;
        immersion.classList.remove("immersion");
        listen.classList.remove("listening");
    }
    console.log(sts);
}


async function statusFLOAT() {
    if (listening) {
        listeningFLOAT()    
        return;
    }
    let status = await getRequest("/FLOAT/status");
    const serial = document.getElementsByClassName("status SERIAL")[0];
    const ready = document.getElementsByClassName("status READY")[0];
    const drop = document.getElementsByClassName("status DROP");
    const immersion = document.getElementsByClassName("status IMMERSION")[0];
    const listen = document.getElementsByClassName("status LISTENING")[0];
    if (!status.status) status = await startFloat();
    console.log(status);
    sts = status.text.split("|");
    for (let i = 0; i < sts.length; i++) {
        switch (sts[i].trim()) {
            case "CONNECTED":
                serial.classList.add("on");
                ready.classList.remove("on");                
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                mux = 0;
                break;

            case "CONNECTED&READY":
                serial.classList.add("on");
                ready.classList.add("on");                
                for (let i = 0; i < drop.length; i++) drop[i].classList.add("enabled");
                mux = 1;
                break;
            case "IMMERSION":
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                mux = 0;
                immersion.classList.add("immersion");
                break;
            case "UPLOAD_DATA":
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                mux = 0;
                listen.classList.add("listening");
                listening = 1;
                listeningFLOAT();
            case "DATA_ABORTED":
                mux = 0;
                break
            case "NO USB":
                serial.classList.remove("on");
                ready.classList.remove("on");
                for (let i = 0; i < drop.length; i++) drop[i].classList.remove("enabled");
                mux = 0;
            
        }
    }
}

let msgs = ["GO", "SEND_DATA_ABORT", "SWITCH_AUTO_MODE", "DATA_ABORT", "TRY_UPLOAD"]

async function msg(e, msg_id) {
    if (!mux) {
        console.log("NOT READY FOR MSG");
        return;
    }
    mux = 0;
    const data = await fetch(`FLOAT/msg?msg=${msgs[msg_id]}`);
    if (data.status == 201) mux = 1;
    else alert("Is USB cable connected?")
}
