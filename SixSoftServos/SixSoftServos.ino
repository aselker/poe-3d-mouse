#include "softServo.h"
#include "Arduino.h"


const int enablePins[] = {3,4,5,6,9,10};
const int aPins[] = {2,7,11,33,31,28};
const int bPins[] = {13,8,12,32,30,27};
const int potPins[] = {A0, A2, A4, A6, A8, A10};

const float kp = 10, ki= 7, kd = 2;

softServo servos[6];

const int center = 512, motionRange = 0; //Out of 1024
const float speed = 0.2; //Roughly(?) how many cycles per second to move
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

}

void loop() {
  
  for(int i = 0; i < 6; i++) {
    int phase = sin(float(millis())/1000*speed*2*PI);
    int angle = center + (phase*motionRange);
    servos[i].setPos(angle);
    //servos[i].setPower(255); //Actually sets it to maxPower
    servos[i].update();
    /*Serial.print(angle); Serial.print("\t"); */Serial.print(servos[i].getPos());  Serial.print("\t");
  }
  Serial.println("");
  
  
  delay(10);

}
