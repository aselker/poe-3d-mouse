#include "softServo.h"
#include "Arduino.h"


const int enablePins[] = {10, 25, 4, 5, 6, 9};
const int aPins[] = {28, 2, 7, 11, 33, 31};
const int bPins[] = {27, 13, 8, 12, 32, 30};
const int potPins[] = {A10, A0, A2, A4, A6, A8};
const int centerPos[] = {700, 770, 700, 750, 750, 750};
int angle;
String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete



const float kp = 10, ki= 5, kd = 3;

const int buttonPin = 24;
const int debounceTime = 20; //milliseconds
long unsigned int buttonTime = 0; //The time it was last pressed
bool buttonIsPressed = false;
bool powerMotors;

softServo servos[6];

String strIn = "";


void setup() {

  Serial.begin(115200);
  powerMotors = false;
  inputString.reserve(200);

  for(int i = 0; i < 6; i++) {
    servos[i].setup(enablePins[i], aPins[i], bPins[i], potPins[i], kp, ki, kd, false, false); //None are reversed, for testing purposes

  }
  
  servos[0].potReversed = false;
  servos[0].motorReversed = false;

  servos[1].potReversed = true;
  servos[1].motorReversed = false;

  servos[2].potReversed = false;
  servos[2].motorReversed = false;

  servos[3].potReversed = true;
  servos[3].motorReversed = false;

  servos[4].potReversed = true;
  servos[4].motorReversed = false;
  
  servos[5].potReversed = false;
  servos[5].motorReversed = true;

  pinMode(buttonPin, INPUT_PULLUP);
  for (int i = 0; i < 6; i++) {
    servos[i].setPower(0);
  }
  powerMotors = false;

}

void loop() {

  
    Serial.println(inputString );
      if (stringComplete == true)
      {
      for (int i = 0; i < 7; i++) {
        
        int pos = strIn.indexOf(',');
        
        if (pos == -1) { //If we didn't find a match, use the rest of the string
        //  servos[i].setPos(centerPos[i] - 5*strIn.toInt());
          break; //Can't read any more
        } //End if no match
        
        String substr = strIn.substring(0,pos); //Select the first part
        Serial.println(substr);
        if (i == 0) // mesage starts with motors on comand
        {
          if( substr == "1.0")
          {
              powerMotors = true;
          }
          else
          {
            powerMotors = false;
          }
        }
       
        if (i != 0)
        {
          if (powerMotors)
            servos[i-1].setPos(centerPos[i-1] - 5*substr.toInt());
          else
            servos[i-1].setPower(0);
        }
        strIn.remove(0, pos+1); //Remove that many chars, including the comma
      } //end for 
      strIn = "";
    } 
  

  for (int i = 0; i < 6; i++) {
    servos[i].update();
    Serial.print((servos[i].getPos()-centerPos[i])/-5); //Print the actual position, then a comma
    if (i != 5) Serial.print(",");
  }

/*
  if (digitalRead(buttonPin) == LOW) {
    if (!buttonIsPressed) {
      buttonIsPressed = true;
      Serial.println("1"); //It just got pressed
    } else Serial.println("0"); //No change

    buttonTime = millis();
  } else if (millis() - buttonTime > debounceTime) {
    if (buttonIsPressed) {
      buttonIsPressed = false;
      Serial.println("-1"); //Just got released
    } else Serial.println("0"); //No change
  }
*/
  Serial.println("");
  
  
  delay(10);

}
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
