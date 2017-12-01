// Library for working with gutted hobby servos

#ifndef SOFTSERVO_H
#define SOFTSERVO_H
#include "Arduino.h"

//using namespace std;

class softServo {

  public:
    softServo(); //Default constructor, for making lists
    softServo(int enablePin, int aPin, int bPin, int potPin, float kp, float ki, float kd, bool isReversed);

    void setup(int enablePin, int aPin, int bPin, int potPin, float kp, float ki, float kd, bool isReversed);
    //There are better ways to move these vars -- initializer lists and tuples -- but they require c++11

    void update(); //Actually reads the pot / sets the motor power; call regularly for best results

    void setPower(int power); //Set motor power, ignore pot

    void setPids(float kp, float ki, float kd); //Reset the pid tuning
    void setPos(int pos); //Go to a position, using current pids. Position is in whatever unit the Arduino uses for analog sensing (usually 0-1023 for full range).
    int getPos(); //Where is it *actually*?

  private:

    static const int winLen = 1024, maxPower = 96, posRange = 1023;

    bool pinsInitialized, isReversed;
    int enablePin, aPin, bPin, potPin;

    bool isPos; //True when we're trying to get to a position
    int power; //How hard we're pushing right now -- reset every update if isPos
    int goalPos; //If isPos, try to go here

    float kp, ki, kd; //Gains

    int window[winLen], lastError, winPos, total, pos; //Some state

    long unsigned int lastTime, loopTime; //The time the last loop finished, and how long it took


};

#endif
