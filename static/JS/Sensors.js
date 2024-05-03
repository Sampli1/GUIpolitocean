var XAXISRANGE = 10000
var TICKINTERVAL = 1000
var lastDate = 100
var data = [];
var options = {
    series: [{
        data: data.slice()
    }],
    chart: {
        id: 'realtime',
        height: 130,
        type: 'line',
        toolbar: {
            show: false
        },
        animations: {
            enabled: false
        },
        zoom: {
            enabled: false
        },
        offsetX: 0
    },
    dataLabels: {
        enabled: true
    },
    stroke: {
        curve: 'smooth'
    },
    title: {
        text: 'Tensione 12V',
        align: 'left'
    },
    markers: {
        size: 0
    },
    xaxis: {
        type: 'datetime',
        range: XAXISRANGE,

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
        max: 100
    },
    legend: {
        show: false
    },
};




function getNewSeries(baseval, yrange) {
    var newDate = baseval + TICKINTERVAL;
    lastDate = newDate
    for(var i = 0; i< data.length - 10; i++) {
        // IMPORTANT
        // we reset the x and y of the data which is out of drawing area
        // to prevent memory leaks
        data[i].x = newDate - XAXISRANGE - TICKINTERVAL
        data[i].y = 0
        data.shift()
    }
    data.push({
        x: newDate,
        y: Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
    })
}

let charts = [];

function startGraph() {
    let n_charts = 1;
    // charts = [
        // new ApexCharts(document.querySelector("#chart_12v"), {...options, title: {text: "Tensione 12V"}}),
        // new ApexCharts(document.querySelector("#chart_5v"), {...options, title: {text: "Tensione 5V"}}), 
        // new ApexCharts(document.querySelector("#chart_pres"), {...options, title: {text: "Pressione"}}),
        // new ApexCharts(document.querySelector("#chart_temp"), {...options, title: {text: "Temperatura"}})
    // ];
    charts = [ 
        new ApexCharts(document.querySelector("#chart_pres"), {...options, title: {text: "Pressione"}}),
    ]
    for (let i = 0; i < n_charts; i++) charts[i].render();

    window.setInterval(function () {
        getNewSeries(lastDate, {
            min: 10,
            max: 90
        });
        for (let i = 0; i < n_charts; i++) charts[i].updateSeries([{data: data}]);
    }, 500)
}


const client = mqtt.connect("mqtt://127.0.0.1:8080");

client.on("connect", () => {
    console.info("[MQTT] Ready");
    client.subscribe("presence", (err) => {
        if (!err) {
            client.publish("test_topic", "Hello mqtt");
        }
    });
    startGraph();
});

client.on("message", (topic, message) => {
  // message is Buffer
  console.log(message.toString());
  client.end();
});

client.on('error', (error) => {
  try {
    console.error('MQTT Error:', error);
  } catch (err) {
    console.error('Error in error handler:', err);
  }
});