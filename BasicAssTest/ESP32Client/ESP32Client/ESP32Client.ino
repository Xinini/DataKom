#include <SocketIoClient.h>
#include <WiFi.h>

SocketIoClient webSocket;

const char * ssid = "Get-2G-DD0FF1";
const char * password = "BH7DPBXU4U";

const char * webServerHost = "192.168.0.146";
int webServerPort = 3000;

const int readPin = 34;

unsigned long lastMillis;

void socketConnected(const char * payload, size_t length){
  Serial.println("Socket connection established");
}

bool millisDelay(unsigned int delay){
  unsigned long deltaTime = millis() - lastMillis;
  if(deltaTime > delay){
    lastMillis = millis();
    return true;    
  } else {
    return false;
    }
  }
  

void emitData(int pin, int data){ //Bruk millis
  if(millisDelay(1000)){
    char buf_char[5]; //Length of pinVal + null
    String message = String(data);
    Serial.println(data);
    Serial.println(message);
    message.toCharArray(buf_char, 5);
    Serial.println(buf_char);
    webSocket.emit("pinVal", buf_char);
  }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  lastMillis = millis();
  
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("Establishing connection...");
    delay(1000);
  }
  Serial.println("Connected");
  Serial.println(WiFi.localIP());
  pinMode(readPin, INPUT);

  webSocket.on("connection", socketConnected);
  webSocket.begin(webServerHost, webServerPort);
  
}

void loop() {
  webSocket.loop();
  Serial.println(analogRead(readPin));
  emitData(readPin, analogRead(readPin));
}
