/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo S1;
Servo S2;
Servo S3;
Servo S4;
Servo S5;
Servo S6;
int theta = 0;
float delta = 0;
float hrange = 0;
float lrange = 0;
unsigned long timer = 0;
unsigned long up = 0;
const float pi = 3.14;
unsigned long down = 0;
int last = 0;
int ratio = 0;
int pos = 0;    // variable to store the servo position

void setup() {
  S1.attach(11);
  S2.attach(10);
  S3.attach(9);
  S4.attach(6);
  S5.attach(5);
  S6.attach(3);// attaches the servo on pin 9 to the servo object
  up = 1;
  down = 0;
  lrange = 0;
  delta = 0;

  Serial.begin(9600);
  theta = 90;
  hrange = 50;
  ratio = 5;
 // 5 degrees per second
  last = 0;
}

void loop() {
  timer = millis();
 float delta =120- (sinWave(120, timer, 0.25 , 0, 30));
//  S1.write(93.5729);
//  S2.write(180-75.803);
//  S3.write(74.6268);
//  S4.write(180-91.7375);
//  S5.write(91.5439);
//  S6.write(180-94.2721);
   S1.write(180-79.405);
  S2.write(79.405);
  S3.write(180-79.405);
  S4.write(79.405);
  S5.write(180-79.405);
  S6.write(79.405);
 
 
    Serial.println(theta-delta);
 
    
}
float sinWave(int start, float Time, float omega, float phase, int stroke) {
  // returns the angle for a servo motor based on time
  //start is the sevo's center position
  //time is the time the program has been running
  //omega is the feq of the osilations
  //plase is the phase offset in rad
  //stroke is the aplidtude of the wave
  // angle should be a sine wave
  // phase is input as wavelenth and is converted into rad
  
  float theta = fmod(( 2.0*pi * Time / 1000.0), (2.0* pi/omega)); 
  float servoPos = start + stroke * sin(omega * theta + phase); 
  return servoPos;
  
}
 

  
 /* 
  for (int i = lrange; i < hrange; i++){
    delta =i;
  
  //R means that as the angle increases the servo goes down
  S1.write(theta-delta/10);
  S2.write(theta+ delta/10);
  S3.write(theta-delta/10);
  S4.write(theta+delta/10);
  S5.write(theta-delta/10);
  S6.write(theta+delta/10);
  delay(10);
  }
   for (int i = hrange; i > lrange; i--){
    delta =i;
  
  //R means that as the angle increases the servo goes down
  S1.write(theta-delta/10);
  S2.write(theta+ delta/10);
  S3.write(theta-delta/10);
  S4.write(theta+delta/10);
  S5.write(theta-delta/10);
  S6.write(theta+delta/10);
  delay(10);
  }
  */


