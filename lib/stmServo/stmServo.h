// Library for working with gutted hobby servos

#ifndef STMSERVO_H
#define STMSERVO_H

#include "Arduino.h"

using namespace std;


class stmServo {

  public:
    stmServo(int enablePin, int aPin, int bPin, int potPin, float kp, float ki, float kd);
    //There are better ways to move these vars -- initializer lists and tuples -- but they require c++11

    void update(); //Actually reads the pot / sets the motor power; call regularly for best results

    void setPower(int power); //Set motor power, ignore pot

    void setPids(float kp, float ki, float kd); //Reset the pid tuning
    void setPos(int pos); //Go to a position, using current pids
    int getPos(); //Where is it *actually*?

  private:

    static const int winLen = 1024, maxPower = 96; //Running at 9v for now -- don't go above around 128

    USBSerial usb; //For debug

    int enablePin, aPin, bPin, potPin;

    bool isPos; //True when we're trying to get to a position
    int power; //How hard we're pushing right now -- reset every update if isPos
    int goalPos; //If isPos, try to go here

    float kp, ki, kd; //Gains

    int window[winLen], lastError, winPos, total, pos; //Some state

    long unsigned int lastTime, loopTime; //The time the last loop finished, and how long it took


};

#endif
