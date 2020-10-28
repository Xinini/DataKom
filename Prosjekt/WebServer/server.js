var express = require('express');

// App setup
var app = express();
var server = app.listen(4000, function(){
    console.log('listening for requests on port 4000,');
});

// Static files
app.use(express.static('public'));




/*
var http = require('http');
var express = require('express');
var app = express();

var PORT = 3000;

var server = app.listen(PORT, ()=>{
    console.log("Listening on port: *" + PORT);
});


app.use(express.static('public'));

/*
var io = require('socket.io').listen(server);

io.on('connection', (socket) =>{
    console.log('Client Connected');
    var clientID = socket.id;
    var client = io.sockets.connected[clientID];
    client.emit('connection', ' ');

    console.log("Client ID: " + clientID);


})
*/
