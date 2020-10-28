var http = require('http');
var express = require('express');
var app = express();

var PORT = 3000;

var server = http.createServer(app);
var io = require('socket.io').listen(server);

server.listen(PORT, () =>{
    console.log('listening on port: *' + PORT);
});

io.on('connection', (socket) =>{
    console.log('Client Connected');
    var clientID = socket.id;
    var client = io.sockets.connected[clientID];
    client.emit("connection", " ");
    console.log("Client ID: " + clientID);

    socket.on('pinVal', (pinVal) => {
        console.log(pinVal);
    })

});