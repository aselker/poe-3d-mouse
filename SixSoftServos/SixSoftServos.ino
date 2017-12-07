#include "softServo.h"
#include "Arduino.h"


const int enablePins[] = {25,4,5,6,9,10};
const int aPins[] = {2,7,11,33,31,28};
const int bPins[] = {13,8,12,32,30,27};
const int potPins[] = {A0, A2, A4, A6, A8, A10};
const int centerPos[] ={770,700,750,750,750,700};
int angle;


const float kp = 10, ki= 5, kd = 3;

const int buttonPin = 24;
const int debounceTime = 20; //milliseconds
long unsigned int buttonTime = 0; //The time it was last pressed
bool buttonIsPressed = false;

softServo servos[6];


const int center = 512, motionRange = 100; //Out of 1024
const float speed = 1.5; //Roughly(?) how many cycles per second to move
const float offsets[] = {0, PI/3., 2.*PI/3., PI, 4.*PI/3., 5.*PI/3.};


void setup() {

  Serial.begin(9600);
  

  for(int i = 0; i < 6; i++) {
    servos[i].setup(enablePins[i], aPins[i], bPins[i], potPins[i], kp, ki, kd, false, false); //None are reversed, for testing purposes
  }

  servos[0].potReversed = true;
  servos[0].motorReversed = false;

  servos[1].potReversed = false;
  servos[1].motorReversed = false;

  servos[2].potReversed = true;
  servos[2].motorReversed = false;

  servos[3].potReversed = true;
  servos[3].motorReversed = false;
  
  servos[4].potReversed = false;
  servos[4].motorReversed = true;
  
  servos[5].potReversed = false;
  servos[5].motorReversed = false;

  pinMode(buttonPin, INPUT_PULLUP);
  for (int i = 0; i < 6; i++)
  {
  Serial.print(centerPos[i]);
  servos[i].setPos(centerPos[i]);
  }

}

void loop() {

  if (Serial.available()) {
    String in(Serial.readString());
    //Serial.println(in);
    for (int i = 0; i < 6; i++) {
      int pos = in.indexOf(',');
      Serial.print(i); Serial.print("\t");

      if (pos == -1) { //If we didn't find a match, use the rest of the string
     //   servos[i].setPos(atoi(in.c_str()) * 1023.0 / 180.0); //Set the servo using the entire string
        break; //Can't read any more
      } //End if no match
      
      
      String substr = in.substring(0,pos); //Select the first part
     // Serial.println(substr);
      angle = substr.toInt();
      in.remove(0, pos+1); //Remove that many chars, including the comma
      Serial.print(centerPos[i] - 5*angle); Serial.print("\t");
      servos[i].setPos(centerPos[i] - 5*angle); //Set the servo
      
    } //end for
  } //end if available


  for (int i = 0; i < 6; i++) {
    servos[i].update();
    Serial.print(servos[i].getPos()); Serial.print("\t"); //Print the actual position, then a comma
  }

  if (digitalRead(buttonPin) == LOW) {
    if (!buttonIsPressed) {
      buttonIsPressed = true;
    //  Serial.println("1"); //It just got pressed
    }// else Serial.println("0"); //No change

    buttonTime = millis();
  } else if (millis() - buttonTime > debounceTime) {
    if (buttonIsPressed) {
      buttonIsPressed = false;
    //  Serial.println("-1"); //Just got released
    }// else Serial.println("0"); //No change
  }
  

 /*
  for(int i = 0; i < 6; i++) {
    
    float phase = 0*sin( float(millis())/1000.0*1*2.0*PI );//+ offsets[i] );
    int angle = centerPos[i]+ (phase*motionRange);
    servos[i].setPos(angle);
    //servos[i].setPower(255); //Actually sets it to maxPower
    servos[i].update();
    Serial.print(angle); Serial.print("\t"); Serial.print(servos[i].getPos());  Serial.print("\t");
  }
  */
  Serial.println("");
  
  
  delay(10);

}
