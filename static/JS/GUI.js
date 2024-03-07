let page_now = -1;
let info;
let script = document.currentScript;
let fullUrl = script.src;
let jsonUrl = fullUrl.replace("JS/GUI.js", "info.json");


document.addEventListener('DOMContentLoaded', async function () {
    const data = await fetch(jsonUrl, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    });
    info = await data.json();
})


async function change(page) {
    if (info.pages[page] == page_now) return;
    page_now = info.pages[page];
    const newpage = await (await fetch(page)).text();
    let parser = new DOMParser();
    let html = parser.parseFromString(newpage, "text/html");
    let wh = document.querySelectorAll(".window")[0];
    wh.replaceChildren(html.body.firstChild);
}


function switching(id) {
    let n_camera = `${id.match(/\d+/)[0]}`;
    console.log(n_camera);
    if (info["cameras"][n_camera]["status"] == 0) return;
    let z = -1;
    for (let i = 0; i < info["n_cameras"] && z == -1; i++) if (info["cameras"][`${i}`]["status"] == 0) z = i;
    let camera_p = document.querySelector(".camera_p");
    let camera_s = document.querySelectorAll(`.camera_s`);
    let target, deploy;
    console.log(camera_s);
    camera_s.forEach((el) => {
        if (el.firstElementChild.id == `c${n_camera}`) {
            target = el.firstElementChild;
            deploy = el;
        }
    });
 
    let sub = document.querySelectorAll(".div3");

    console.log(target);
    camera_p.append(target);
    deploy.append(camera_p.firstElementChild);

    // devi aggiornare i valori del cazzo
}

async function onoff(id) {
    let wh = document.querySelectorAll(`#c${id.match(/\d+/)[0]}`)[0];
    console.log(wh);
    info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"] = !info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"];
    if (info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"] == 1) wh.className = wh.className.replace(" hide", "");
    else wh.className += " hide";
}
