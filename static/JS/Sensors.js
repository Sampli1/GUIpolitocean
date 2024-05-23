var XAXISRANGE = 10000
var lastDate = [0]
var data = [[]];
var options = {
    series: [{
        data: data.slice()
    }],
    chart: {
        id: 'realtime',
        height: 300,
        width: 400,
        type: 'line',
        toolbar: {
            show: false
        },
        animations: {
            enabled: false
        },
        zoom: {
            enabled: true
        },
        offsetX: 0
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    title: {
        text: 'Tensione 12V',
        align: 'left',
        style: {
            colors: ["#ffffff"],
            color: "#ffffff"
        }
    },
    markers: {
        size: 0
    },
    xaxis: {
        type: 'datetime',
        range: XAXISRANGE,
        labels: {
            style: {
                colors: ['#ffffff', '#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff','#ffffff']
            }
        }
    },
    annotations: {
        xaxis: [
            {
                show: false
            }
        ],
        yaxis: [
            {
                show: false
            }
        ]
    },
    yaxis: {
        max: 5.5,
        min: -1,
        labels: {
            style: {
                colors: ['#ffffff', '#ffffff','#ffffff','#ffffff','#ffffff','#ffffff']
            }
        }
    },
    legend: {
        show: false
    }
};



var TICKINTERVAL = 1000
function getNewSeries(baseval, newP, index, data_n) {
    console.log(data_n)
    var newDate = baseval + TICKINTERVAL;
    lastDate[index] = newDate;
    for(var i = 0; i < data_n.length - 10; i++) {
        // IMPORTANT
        // we reset the x and y of the data which is out of drawing area
        // to prevent memory leaks
        data_n[i].x = newDate - XAXISRANGE - TICKINTERVAL
        data_n.shift()
    }
    data_n.push({
        x: newDate,
        y: newP
    })
}

let charts = [];

function startGraph() {
    // charts = [
        // new ApexCharts(document.querySelector("#chart_12v"), {...options, title: {text: "Tensione 12V"}}),
        // new ApexCharts(document.querySelector("#chart_5v"), {...options, title: {text: "Tensione 5V"}}), 
        // new ApexCharts(document.querySelector("#chart_pres"), {...options, title: {text: "Pressione"}}),
        // new ApexCharts(document.querySelector("#chart_temp"), {...options, title: {text: "Temperatura"}})
    // ];
    charts = [ 
        new ApexCharts(document.querySelector("#chart_pres"), {...options, title: {text: "Pressione"}}),
    ]
    for (let i = 0; i < charts.length; i++) charts[i].render();
}

const mqtt_c = mqtt.connect("mqtt://10.0.0.254:9000");
// const mqtt_c = mqtt.connect("mqtt://127.0.0.1:8080");

mqtt_c.on("connect", () => {
    console.info("[MQTT] Ready");
    mqtt_c.subscribe("depth/");
    mqtt_c.subscribe("debug/");
    startGraph()
});

mqtt_c.on('message', function (topic, message) {
    let text = message.toString()
    switch (topic) {
        case "depth/":
            console.log(text)
            console.log(parseFloat(text))
            getNewSeries(lastDate[0], parseFloat(text), 0, data[0]);
            charts[0].updateSeries([{data: data[0]}]);
            break;
        case "debug/":
            console.log(text)
  }
})

mqtt_c.on('error', (error) => {
  try {
    console.error('MQTT Error:', error);
  } catch (err) {
    console.error('Error in error handler:', err);
  }
});