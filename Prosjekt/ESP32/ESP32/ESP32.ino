#include <SocketIoClient.h>
#include <WiFi.h>

SocketIoClient webSocket;

const char * ssid = "Get-2G-DD0FF1";
const char * password = "BH7DPBXU4U";

const char * webServerHost = "192.168.0.111";
int webServerPort = 3000;


void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("Establishing connection...");
    delay(1000);
  }
  Serial.println("Connected");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

}
