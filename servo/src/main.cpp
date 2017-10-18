#include "Arduino.h"
#include "EEPROM.h"
 
#define LED_BUILTIN PC13

const int goalPos = 2048;

const float kp = 10, ki= 1, kd = 10;
const int winLen = 128;
const int maxPower = 128; //Running at 9v for now
 
const int enablePin = PB0;
const int aPin = PA7;
const int bPin = PA6;
const int potPin = PB1;

int window[winLen], winPos = 0, total = 0; //The last few readings, and a pointer to where the circular buffer's ends are, and a total we keep for speed
int lastError; //The error from the last loop, for D gain

long unsigned int lastTime, loopTime; //The time the last loop finished, and how long it took

USBSerial usb;

void setup()
{
  pinMode(enablePin, OUTPUT);
  pinMode(aPin, OUTPUT);
  pinMode(bPin, OUTPUT);
  pinMode(potPin, INPUT);

  for (int i = 0; i < winLen; i++) window[i] = 0; //Initialize with no integral

  usb.begin(9600);

}
 
void loop()
{

  int error = analogRead(potPin) - goalPos;

  winPos++; //Go to the next position in the buffer
  winPos = winPos % winLen;
  total += error; //Add the value being added
  total -= window[winPos]; //Remove the value being removed
  window[winPos] = error; //Add the new value, knocking out an older one

  float avg = total / winLen;

  int power = ( (error * kp) + (avg * ki) + ((error - lastError) / lastTime * kd) ) * (255.0/4096.0);

  usb.println("P: " + String(error * kp) + " I: " + String(avg * ki) + "D: " + String((error - lastError) / lastTime * kd) );

  lastError = error;

  if (power > maxPower) power = maxPower;
  if (power < -maxPower) power = -maxPower;

  analogWrite(enablePin, abs(power));
  digitalWrite(aPin, (power>0) ? HIGH : LOW);
  digitalWrite(bPin, (power>0) ? LOW : HIGH);


  delay(5); //Make the cycle time less unstable (?)

  loopTime = millis() - lastTime; //For decrementing turn timer
  lastTime = millis(); //So we'll know how long the next loop takes

}
