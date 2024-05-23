function Task1Loader() {
    document.getElementById('fileInput').addEventListener('change', function(event) {
        uploadFile(event);
    });
}

function publishPlot(data) {
    const tab = document.getElementsByClassName("task1_res")[0];
    if (tab.hasChildNodes()) tab.removeChild(tab.firstChild);
    let img = document.createElement('img');
    let div = document.createElement('div');
    div.classList.add('task1_report');
    if (data.data != "NO_DATA") {
        img.src = "data:image/jpeg;charset=utf-8;base64," + data.data;
        div.append(img);
        tab.appendChild(div);
    }
    else {
        let p = document.createElement('p');
        div.append(p);
        p.innerText = `NO DATA`;
        tab.appendChild(div);
    }
}

function uploadFile(event) {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
        const formData = new FormData();
        formData.append('file', file);
        fetch('/TASK_1/file', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            document.getElementById('fileInfo').innerHTML = `Success!`;
            console.log(data);
            publishPlot(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('fileInfo').innerHTML = `Error`;
        });
    } else {
        alert('Not a CSV');
    }
    // delete buffer upload
    event.target.value = '';
    if (e.target.value) {
        e.target.type = 'text';
        e.target.type = 'file';
    }
}

async function statusPhotogrammetry() {
    data = await getRequest("/TASK_2/status");
    console.log(data);
}


async function startPhotogrammetry() {
    data = await getRequest("/TASK_2/start");
    setInterval(statusPhotogrammetry, 2000);
}