#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char *ssid = "tejgold@ClassicTech";
const char *pass = "ngnl@2021";
const char *host = "192.168.254.3";
const char *port = "5000";

WiFiClient wificlient;

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
delay(10);

Serial.println();
Serial.print("Connecting to ");
Serial.println(ssid);
WiFi.begin(ssid, pass);

while(WiFi.status() != WL_CONNECTED){
  delay(500);
  Serial.print(".");
}
Serial.println("");
Serial.println("WiFi connected");
Serial.print("IP address: ");
Serial.println(WiFi.localIP());
}

void loop() {
  HTTPClient http;
//  "http://192.168.254.13:5000/esp"
  String getUrl = "http://" + String(host) + ":" + String(port) + "/esp";
  http.begin(wificlient, getUrl);
  int httpCode = http.GET();
  if(httpCode > 0 ){
    if(httpCode == HTTP_CODE_OK){
      String payload = http.getString();
      Serial.println(payload);  
    }
  }
  else{
    Serial.printf("[HTTP] GET... failed error: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();
  delay(1000);
}
/*
 * Source :
 * https://create.arduino.cc/projecthub/jayesh_nawani/read-website-data-using-esp8266-193636
 * https://stackoverflow.com/questions/67702822/error-call-to-httpclientbegin-declared-with-attribute-error-obsolete-api
 * https://simple-circuit.com/arduino-esp-01-esp8266-programming/
 * https://www.geekstips.com/esp8266-arduino-tutorial-iot-code-example/
 */
//*/
