#include "stmServo.h"

stmServo::stmServo(int enablePin, int aPin, int bPin, int potPin, float kp, float ki, float kd) {

  this->enablePin = enablePin;
  this->aPin = aPin;
  this->bPin = bPin;
  this->potPin = potPin;

  pinMode(enablePin, OUTPUT);
  pinMode(aPin, OUTPUT);
  pinMode(bPin, OUTPUT);
  pinMode(potPin, INPUT);

  setPids(kp, ki, kd); //Also clears I buffer

  setPower(0); 

  usb.begin(9600);


}

void stmServo::setPids(float kp, float ki, float kd) { //Reset the pid tuning

  this->kp = kp;
  this->ki = ki;
  this->kd = kd;

  for (int i = 0; i < winLen; i++) window[i] = 0; //re-init integral
  winPos = 0;
  total = 0;
}

void stmServo::setPower(int power) {

  this->power = power;
  isPos = false;

}

void stmServo::setPos(int pos) {


  if (!isPos) { //If switching from power to position, re-init integral
    for (int i = 0; i < winLen; i++) window[i] = 0;
    winPos = 0;
    total = 0;
  }

  this->goalPos = pos;
  isPos = true;

}

int stmServo::getPos() {

  return pos;

}

void stmServo::update() {

  pos = analogRead(potPin);

  if (isPos) {

    int error = pos - goalPos;

    winPos++; //Go to the next position in the buffer
    winPos = winPos % winLen;
    total += error; //Add the value being added
    total -= window[winPos]; //Remove the value being removed
    window[winPos] = error; //Insert the new value, knocking out an older one

    float avg = total / winLen;

    int p = error * kp;
    int i = avg * ki;
    int d = float(error - lastError) / float(loopTime) * kd;

    usb.println("P: " + String(p) + " I: " + String(i) + "D: " + String(d) );
    usb.println("Last error: " + String(lastError) + " Current error: " + String(error) + " Last loop time: " + String(loopTime));

    power = (p + i + d) * (255.0/1023.0); //2047 for stm32, 1023 for most Arduinos

    lastError = error;

  } //End if isPos

  if (power > maxPower) power = maxPower;
  if (power < -maxPower) power = -maxPower;

  analogWrite(enablePin, abs(power));
  digitalWrite(aPin, (power>0) ? HIGH : LOW);
  digitalWrite(bPin, (power>0) ? LOW : HIGH);

  loopTime = millis() - lastTime; //For decrementing turn timer
  lastTime = millis(); //So we'll know how long the next loop takes


}
