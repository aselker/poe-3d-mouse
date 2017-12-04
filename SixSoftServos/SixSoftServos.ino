#include "softServo.h"
#include "Arduino.h"


const int enablePins[] = {3,4,5,6,9,10};
const int aPins[] = {2,7,11,33,31,28};
const int bPins[] = {13,8,12,32,30,27};
const int potPins[] = {A0, A2, A4, A6, A8, A10};

const float kp = 10, ki= 7, kd = 2;

softServo servos[6];

const int center = 512, motionRange = 100; //Out of 1024
const float speed = 0.2; //Roughly(?) how many cycles per second to move
const float offsets[] = {0, PI/3., 2.*PI/3., PI, 4.*PI/3., 5.*PI/3.};

void setup() {

  for(int i = 0; i < 6; i++) {
    servos[i].setup(enablePins[i], aPins[i], bPins[i], potPins[i], kp, ki, kd, false, false); //None are reversed, for testing purposes
  }

}

void loop() {

  for(int i = 0; i < 6; i++) {
    int phase = sin(float(millis())/1000*speed*2*PI + offsets[i]);
    servos[i].setPos(center + (phase * motionRange/2));
    servos[i].update();
  }
  
  delay(10);

}
