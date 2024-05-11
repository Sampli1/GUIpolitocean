let page_now;

addEventListener("resize", (event) => {
    let h = window.innerHeight;
    let w = window.innerWidth;
    let body = document.getElementsByTagName('body')[0];
    body.style.width = `${w}px`; 
    body.style.height = `${h}px`;
});

async function change(page) {
    if (page == page_now) return;
    if (page_now !== "home") document.getElementsByClassName(page_now)[0].classList.toggle("hide");
    document.getElementsByClassName(page)[0].classList.toggle("hide");
    page_now = page;
}


function switching(id) {
    let n_camera = `${id.match(/\d+/)[0]}`;
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
    camera_p.append(target);
    deploy.append(camera_p.firstElementChild);
    info["cameras"][n_camera]["status"] = 0;
    info["cameras"][z]["status"] = 1;
}

async function onoff(id) {
    let wh = document.querySelectorAll(`#c${id.match(/\d+/)[0]}`)[0];
    console.log(wh);
    console.log(info)
    info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"] = !info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"];
    if (info["cameras"][`${id.match(/\d+/)[0]}`]["enabled"] == 1) wh.className = wh.className.replace(" hide", "");
    else wh.className += " hide";
}


function styles(ev){
    const new_style_element = document.createElement("style");
    new_style_element.textContent = "html { color: white; }"
    ev.target.contentDocument.head.appendChild(new_style_element);
}

