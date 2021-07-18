#include <SoftwareSerial.h>

/*
   rx - digital pin 2
   tx - digital pin 3
*/
//just a test code and ruff idea need to implement on real board
int fanPin = 12;
int lightPin = 13;
bool fanState = false;
bool lightState = false;
String readString;
bool receivedString = false;

SoftwareSerial mySerial(2, 3); //rx, tx

bool isCmdInString(char *command) {
  //checks the global variable readString which is updated everytime in the program
  bool isPresent = (readString.indexOf(command) != -1) ? true : false;
  return isPresent;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(lightPin, OUTPUT);
  Serial.begin(115200);
  mySerial.begin(115200);
  delay(10);
}

// TODO :
// 1. need to assign pins
// 2. add implementation with corresponding index
// 3. test the program in real board...
void loop() {
  // put your main code here, to run repeatedly:
  while (mySerial.available()) {
    if (mySerial.available() > 0) {
      char c = mySerial.read();
      if (isControl(c)) {
        break;
      }
      readString += c;
    }
    receivedString = true;
  }
  if (receivedString) {
    Serial.print("received String : ");
    Serial.println(readString);
    if (isCmdInString("P")) {
      if (isCmdInString("0")) {
        digitalWrite(lightPin, false);
        delay(1000);
        //TODO when prediction is word in index 0.
        Serial.println("value zero!!!");
      }
      else if (isCmdInString("1")) {
        digitalWrite(lightPin, true);
        delay(1000);
        //TODO when prediction is word in index 1.
        Serial.println("value one!!!");
      }
      else if (isCmdInString("2")) {
        //TODO when prediction is word in index 2.
        Serial.println("value two!!!");
      }
      else if (isCmdInString("3")) {
        //TODO when prediction is word in index 3.
        Serial.println("value three!!!");
      }
      else if (isCmdInString("4")) {
        //TODO when prediction is word in index 4.
        Serial.println("value four!!!");
      }
      else {
        Serial.println("No Command Received");
      }
      delay(1000);
    }
    else {
      Serial.println("No Command Received");
    }
    readString = "";
    delay(1000);
    receivedString = false;
  }
}

/*
   https://www.electroniclinic.com/serial-communication-between-two-arduino-boards/
*/
