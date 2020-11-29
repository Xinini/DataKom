const socket = io.connect("http://192.168.0.111:4000", {secure: false});

var xLabels = [];
var lightValues = [];

socket.emit("getStartData");


function onOff(){
    socket.emit("toggleLight");
}

function chooseMode(mode){
    socket.emit("chooseMode", mode);
}

socket.on("modeUpdate", (mode)=>{
    document.getElementById("mode").innerHTML = "Current mode: " + mode
});

function setTime(){
    var start = document.getElementById("start-time").value;
    var end = document.getElementById("end-time").value;
    socket.emit("setTime", {
        start: start,
        end, end
    });

}

socket.on("lightUpdate", (state)=>{
    if(state == 1){
        document.getElementById("state").innerHTML = "Current state: ON";
    } else if(state == 0){
        document.getElementById("state").innerHTML = "Current state: OFF";
    }
});

socket.on("newChartData", (chartData)=>{
    myChart.data.labels = Object.keys(chartData);
    myChart.data.datasets[0].data = Object.values(chartData);
    myChart.update();

    let lastVal = Object.values(chartData)[Object.values(chartData).length - 1];
    document.getElementById("value").innerHTML = "Current value: " + lastVal;
});






var chart = document.getElementById('light-chart');
var myChart = new Chart(chart, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Light Level ',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        legend: {
            labels:{
                fontColor: "#000000"
            }
        },
        scales: {
            yAxes: [{
                gridLines: {color: "#000000"},
                ticks: {
                    beginAtZero: true,
                    fontColor: "#000000"
                }
            }],
            xAxes:[{
                gridLines: {color: '#000000'},
                ticks: {
                    fontColor: "#000000"
                }
            }]
        },
        maintainAspectRatio: false
    }
});


