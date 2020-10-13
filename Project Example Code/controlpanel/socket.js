var socket = io.connect('192.168.1.1:2520', {secure: false});

socket.on('connect',function() {
    console.log('Client has connected to the server!');
});

socket.on('clientConnected',function(id, ip) {
    console.log('Client recevied ID: ' + id);
    console.log("Client IP: " + ip);

});

/*socket.on('data', function(data) {

    console.log('Data was received: ' + data);
    console.log(Number(data));
    dataArr.push(data);
    //myLineChart.update();

});*/

function changeLEDState(state) {

    socket.emit('changeLEDState', state);
    console.log("changeLEDState called");

}

function changeDriveState(state) {

    socket.emit('changeDriveState', state);
    console.log("changeDriveState called");

}

function changeTurnState(state) {

    socket.emit('changeTurnState', state);
    console.log("changeTurnState called");

}

function changeStopState(state) {

    socket.emit('changeStopState', state);
    console.log("changeStopState called");

}

/*function requestDataFromBoard(intervall) {
    socket.emit('requestDataFromBoard', intervall);
    console.log("requestDataFromBoard was called with intervall: " + intervall);
}*/

