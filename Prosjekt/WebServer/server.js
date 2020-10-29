var express = require('express');



var http = require('http');
var express = require('express');
var app = express();

var PORT = 4000;

var server = app.listen(PORT, ()=>{
    console.log("Listening on port: *" + PORT);
});



app.use(express.static('public'));


var io = require('socket.io').listen(server);


var state = 0;
io.on('connection', (socket) =>{
    console.log('Client Connected');
    var clientID = socket.id;
    var client = io.sockets.connected[clientID];
    client.emit('connection', ' ');

    console.log("Client ID: " + clientID);
    socket.on("toggleLight", function(){
        if(state == 0){
            console.log("lightOn");
            socket.emit("lightOn");
        } else if(state == 1) {
            console.log("lightOff");
            socket.emit("lightOff");
        }
        state = !state;
    })


})
