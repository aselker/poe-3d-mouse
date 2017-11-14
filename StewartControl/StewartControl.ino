#include <Servo.h>

Servo servos[6];
const int servoPins[] = {11, 10, 9, 6, 5, 3};
float lowerLimit = -30; //The lowest position they're allowed to go to

int servoPos[6];

void setup() {

  for (int i = 0; i < 6; i++) {
    servos[i].attach(servoPins[i]); //Attach the servos to their pins
    servoPos[i] = 90;
    servos[i].write(servoPos[i]);
  }

  Serial.begin(9600);
}

void loop() {

  if (Serial.available()) {
    for (int i = 0; i < 6; i++) {
      String input = "";
      while (Serial.available()) {
        input += Serial.read();
        if (input[input.length()-1] == ','|| input[input.length()-1] == "\n") break; //Keep reading till we hit a comma, or the EOL
      }
      if (atoi(input.c_str()) > lowerLimit) { //Limit the range
        if (i % 2 == 0) servoPos[i] = (90.0 + atoi(input.c_str())); 
        else servoPos[i] = (90.0 - atoi(input.c_str()));
      } else {
        if (i % 2 == 0) servoPos[i] = (90.0 + lowerLimit);
        else servoPos[i] = (90.0 - lowerLimit);
      }
    }
  }

  for (int i = 0; i < 6; i++) {
    servos[i].write(servoPos[i]);
    Serial.print(String(servoPos[i]) + ",");
  }
  Serial.println();

  delay(10);
 
}

