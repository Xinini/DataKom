var fs = require('fs');
var http = require('http');
var express = require('express');
var app = express();

//var admin = require("firebase-admin");

var serverPort = 2520;

var server = http.createServer(app);
var io = require('socket.io').listen(server);

//HTTP Server
server.listen(serverPort, function(){
    console.log('listening on *:' + serverPort);
});

//Firebase admin uplink
/*var serviceAccount = require("C:/Users/Administrator/Desktop/testdbServiceAccountKey.json");*/
/*var fAdmin = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://testdb-d11fc.firebaseio.com"
});*/

//var db = fAdmin.database();

io.on('connection', function(socket){
    console.log('a user connected');

    //Client ID
    var clientID = socket.id;
    var client = io.sockets.connected[clientID];
    client.emit("clientConnected", clientID);
    console.log("User ID: " + clientID);

    //Client IP
    var clientIPRAW = client.request.connection.remoteAddress;

    var IPArr = clientIPRAW.split(":",4);
    console.log("User IP: " + IPArr[3]);

    io.emit("clientConnected", clientID, IPArr[3]);

    //Disconnect protocol
    client.on('disconnect', function(){
        console.log("user " + clientID + " disconnected");
    });

    //Change states, drive car, send data to board
    socket.on('changeLEDState', function(state) {

        io.emit('LEDStateChange', state);
        console.log('user ' + clientID + ' changed the LED state to: ' + state);

    });

    socket.on('changeDriveState', function(state) {

        io.emit('DriveStateChange', state);
        console.log('user ' + clientID + ' changed the Drive state to: ' + state);

    });

    socket.on('changeTurnState', function(state) {

        io.emit('TurnStateChange', state);
        console.log('user ' + clientID + ' changed the Turn state to: ' + state);

    });

    socket.on('changeStopState', function(state) {

        io.emit('stopDriving', state);
        console.log('user ' + clientID + ' changed the Stop state to: ' + state);

    });

    //Read data from board
    socket.on('requestDataFromBoard', function(intervall) {

        if(intervall == 0 && tIntervall != undefined) {
            clearInterval(tIntervall);
            console.log('user ' + clientID + ' cleared data request intervall');
        } else {

            console.log('user ' + clientID + ' requested data with intervall (ms): ' + intervall);

            var tIntervall = setInterval(function(){

                io.emit('dataRequest', 0);

            }, intervall);
        }

    });

    socket.on('dataFromBoard', function(data) {

        io.emit('data', data);
        console.log('user ' + clientID + ' gained the data: ' + data);

    });


});