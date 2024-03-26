let dropped = 0;
let ready = 0;

async function statusFLOAT() {
    let response = await fetch("/FLOAT/status");
    let status = await response.json();
    let data;
    if (!status.status) {
        response = await fetch("/FLOAT/start");
        data = await response.json();
        if (!ready) {
            document.getElementsByClassName("status SERIAL")[0].classList.remove("on");
            document.getElementsByClassName("status DROP")[0].classList.remove("enabled");
        }
        ready = 0;
        return;
    }
    if (response.status == 200) {
        console.error(data.code)
        return;
    }
    document.getElementsByClassName("status SERIAL")[0].classList.add("on");
    document.getElementsByClassName("status DROP")[0].classList.add("enabled");
    ready = 1; 
}

function listen() {
    const data = fetch("FLOAT/listen");
}


async function drop(e) {
    console.log(e);
    if (!ready && !dropped) return;
    const data = await fetch("FLOAT/drop");
    if (data.status == 201) {
        dropped = 1;
        e.classlist.toggle("on");
    }
    else {
        alert("Is USB cable connected?")
    }
}