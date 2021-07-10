
bool fanState = false;
bool lightState = false;
String readString;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(10);
}
// TODO : need to assign pins and character 
// just a test code and ruff idea need to implement on real board
void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()){
    if(Serial.available()>0){
      char c = Serial.read();
      if(isControl(c)){
        break;
      }
      readString += c;
    }
  }

  if(readString == "0"){
    fanState ^= true;
    digitalWrite(13, fanState);
    readString = "";
  }
}
