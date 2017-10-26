#include "Arduino.h"

#include <stmServo.h>

#define LED_BUILTIN PC13

using namespace std;


const float kp = 10, ki= 7, kd = 2;
 
const int enablePin = PB0;
const int aPin = PA7;
const int bPin = PA6;
const int potPin = PB1;

stmServo servo(enablePin, aPin, bPin, potPin, kp, ki, kd);

void setup()
{


}
 
void loop()
{

  servo.setPos(2048 + sin(millis() / 1000.0) * 2048);

  servo.update();

  delay(5); //Make the cycle time less unstable (?)

}
