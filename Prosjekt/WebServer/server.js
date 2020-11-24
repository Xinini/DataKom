var express = require('express');
var http = require('http');
var app = express();

var PORT = 4000;

var server = app.listen(PORT, ()=>{
    console.log("Listening on port: *" + PORT);
});

app.use(express.static('public'));

var io = require('socket.io').listen(server);

var state = 0;
var modes = ["alarm", "manual", "sensor"];
var mode = modes[1]; //Default is manual

var start = 0000;
var end = 0001;


io.on('connection', (socket) =>{
    console.log('Client Connected');
    var clientID = socket.id;
    var client = io.sockets.connected[clientID];
    client.emit('connection', ' ');

    console.log("Client ID: " + clientID);
    socket.on("getStartData", ()=>{
        console.log("dataReq0");
        socket.emit("modeUpdate", mode);
        socket.emit("lightUpdate", state);
    });
    
    socket.on("toggleLight", ()=>{
        mode = modes[1];
        state = 1 - state; //Toggles betwewen 0 and 1
        console.log("ToggledLight");
        io.emit("lightUpdate", state);
    });
    socket.on("chooseMode", (modeIndex)=>{
        mode = modes[modeIndex];
        socket.emit("modeUpdate", mode);
    });
    socket.on("setTime", (time)=>{
        start = time.start;
        end = time.end;
        console.log(start);
        console.log(end);
    });

    socket.on("newSensorData", (sensorData) =>{
        console.log(sensorData);
    });
});


setInterval(() => {
    io.emit("getSensorData");
},
10000);

setInterval(()=>{
    if(mode == modes[0]){
        alarm();
    }
},
30*1000);

function alarm(){
    console.log(start + "start");
    console.log(getCurrentTime());
    if (start == getCurrentTime()){
        console.log("lightON");
        state = 1;
        io.emit("lightUpdate", state);
    }
    if (end == getCurrentTime()){
        state = 0;
        io.emit("lightUpdate", state);
    }
}

function getCurrentTime(){ //Function for getting current time in correct format
    let date_ob = new Date(); 
    let currHour = date_ob.getHours().toString();
    let currMin = date_ob.getMinutes().toString();
    if(currHour.length == 1){ //getHours and getMinutes might return a single digit, and does not follow the format
        currHour = "0" + currHour;
    }
    if(currMin.length == 1){
        currMin = "0" + currMin;
    }
    return currHour + currMin;
}