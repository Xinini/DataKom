#include <Arduino.h>
#include <analogWrite.h>

#include <WiFi.h>
#include <WiFiMulti.h>

#include <SocketIoClient.h>

WiFiMulti WiFiMulti;
SocketIoClient webSocket;

//Motor register default
const int ENA = 33; //Motor 1
const int IN1 = 25; //Wheel direction 1
const int IN2 = 26; //Wheel direction 2
const int ENB = 27; //Motor 2 (need 11 for IRRemote)
const int IN3 = 14; //Wheel direction 3
const int IN4 = 12; //Wheel dirlection 4

//const int L1 = 32;
const int M = 32;
//const int R1 = 32;

void event(const char * payload, size_t length) {
  Serial.printf("got message: %s\n", payload);
}

void changeLEDState(const char * LEDStateData, size_t length) {
  Serial.printf("LED State: %s\n", LEDStateData);
  Serial.println(LEDStateData);

  //Data conversion
  String dataString(LEDStateData);
  int LEDState = dataString.toInt();

  Serial.print("This is the LED state in INT: ");
  Serial.println(LEDState);
  digitalWrite(18, LEDState);
  //Motors(LEDState);//LED on = engines on
}

void changeDriveState(const char * DriveStateData, size_t length) {
  Serial.printf("Drive State: %s\n", DriveStateData);
  Serial.println(DriveStateData);

  //Data conversion
  String dataString(DriveStateData);
  int DriveState = dataString.toInt();

  Serial.print("This is the Drive state in INT: ");
  Serial.println(DriveState);
  Drive(DriveState);
}

void changeTurnState(const char * TurnStateData, size_t length) {
  Serial.printf("Turn State: %s\n", TurnStateData);
  Serial.println(TurnStateData);

  //Data conversion
  String dataString(TurnStateData);
  int TurnState = dataString.toInt();

  Serial.print("This is the Turn state in INT: ");
  Serial.println(TurnState);
  softTurn(TurnState);
}

void stopDriving(const char * StopStateData, size_t length) {
  Serial.printf("Stop State: %s\n", StopStateData);
  Serial.println(StopStateData);

  //Data conversion
  String dataString(StopStateData);
  int StopState = dataString.toInt();

  Serial.print("This is the Stop state in INT: ");
  Serial.println(StopState);
  Stop(StopState); //NEEDS FALSE/0 AS INPUT TO ACTUALLY STOP
}


void dataRequest(const char * DataRequestData, size_t length) {
  
}

void setupMotors() {

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  //Enable motors
  Motors(true);
  
}

void setup() {
    Serial.begin(9600);

    //Set test LED to high on startup
    pinMode(18, OUTPUT);
    digitalWrite(18, HIGH);

    //IR Sensor
    pinMode(M, INPUT);
    analogWriteResolution(M, 10);
    analogReadResolution(10); 
    //End IRsensor test

    Serial.setDebugOutput(true);

    Serial.println();
    Serial.println();
    Serial.println();

      for(uint8_t t = 4; t > 0; t--) {
          Serial.printf("[SETUP] BOOT WAIT %d...\n", t);
          Serial.flush();
          delay(1000);
      }

    WiFiMulti.addAP("SSID", "password");

    while(WiFiMulti.run() != WL_CONNECTED) {
      Serial.println("Not connected to wifi...");
        delay(100);
    }

    Serial.println("Connected to WiFi successfully!");

    webSocket.on("clientConnected", event);
    webSocket.on("LEDStateChange", changeLEDState);
    webSocket.on("DriveStateChange", changeDriveState);
    webSocket.on("TurnStateChange", changeTurnState);
    webSocket.on("stopDriving", stopDriving);

    //Send data to server
    webSocket.on("dataRequest", dataRequest);

    webSocket.begin("nytt.io", 2520);
    
    //MOTORS TEST
    setupMotors();
}

//Enable or disable the motors
void Motors(bool motorState){
  
  digitalWrite(ENA, motorState);
  digitalWrite(ENB, motorState);

  Serial.println("Motors setup");
  
}

//Drive the car forwards or backwards
void Drive(bool Direction){

  if(Direction) {
    Serial.print("w"); //Drive forwards
  } else {
    Serial.print("s"); //Drive backwards
  }
  

  //webSocket.emit("dataFromBoard", "{\"foo\":\"bar\"}");
  
}

//Stop the car
void Stop(bool state){
  
  Serial.print("x"); //stop
}

//Turn the car left or right (turns with the frontwheels)
void softTurn(bool Direction) {
  
  if(Direction) {
    Serial.print("a"); //Drive left
  }
  else {
    Serial.print("d"); //Drive right
  }
}

//Turn the car left or right (turns like a tank)
void hardTurn(bool Direction) {
  
  //Motor A (ENA) 
  digitalWrite(IN1, Direction);
  digitalWrite(IN2, !Direction);

  //Motor B (ENB)
  digitalWrite(IN3, !Direction);
  digitalWrite(IN4, Direction);
  
}

void loop() {
  webSocket.loop();
}
