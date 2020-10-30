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
        state = !state;
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


});
