#include <SocketIoClient.h>
#include <WiFi.h>

SocketIoClient webSocket;

const char * ssid = "NiniPhone";
const char * password = "Damndude";

const char * webServerHost = "192.168.43.109";
int webServerPort = 3000;

const int readPin = 2;

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
  

void emitData(int pin){ //Bruk millis
  if(millisDelay(100)){
    int pinVal = analogRead(pin);
    int * val = pinVal;
    Serial.println(pinVal);
    const char * message = pinVal;
    webSocket.emit("pinVal", message);
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
  emitData(readPin);
}
