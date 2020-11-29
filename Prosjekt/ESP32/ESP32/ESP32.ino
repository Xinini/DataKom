#include <SocketIoClient.h>
#include <WiFi.h>

SocketIoClient webSocket;

const char * ssid = "Get-2G-DD0FF1";
const char * password = "BH7DPBXU4U";

const char * webServerHost = "192.168.0.146";
int webServerPort = 4000;

const int lampPin = 33;
// const int buttonPin;
const int sensorPin = 34; //photoresistor


void lightUpdate(const char * data, size_t length) {
  String dataString = String(data);
  int dataInt = dataString.toInt();
  digitalWrite(lampPin, dataInt);
}

void sendSensorData(const char * data, size_t length) {
  int sensorDataRaw = analogRead(sensorPin);
  char buf_sData[5];
  String message = String(sensorDataRaw);
  message.toCharArray(buf_sData, 5);
  webSocket.emit("newSensorData", buf_sData);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Establishing connection...");
    delay(1000);
  }
  Serial.println("Connected");
  Serial.println(WiFi.localIP());

  pinMode(lampPin, OUTPUT);
  //pinMode(buttonPin, INPUT);
  pinMode(sensorPin, INPUT);

  webSocket.on("lightUpdate", lightUpdate);
  webSocket.on("getSensorData", sendSensorData);

  webSocket.begin(webServerHost, webServerPort);
}

void loop() {
  webSocket.loop();

}
