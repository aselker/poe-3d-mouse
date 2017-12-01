void setup() {

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);

}

void loop() {

  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  for (int i = 0; i < 255; i++) {
    analogWrite(4, i);
    delay(5);
  }
  for (int i = 255; i > 0; i--) {
    analogWrite(4, i);
    delay(5);
  }

  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  for (int i = 0; i < 255; i++) {
    analogWrite(4, i);
    delay(5);
  }
  for (int i = 255; i > 0; i--) {
    analogWrite(4, i);
    delay(5);
  }

}
