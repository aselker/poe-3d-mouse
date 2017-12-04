String data = "99.0,99.0,99.0,99.0,99.0,99.0";
String message = "";
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
message = "1.0,2.0,3.0,30.0,30.0,30.0";
if(Serial.available())
  {
    data = Serial.readStringUntil('\n');;
    message = String(data);
    digitalWrite(13,HIGH);
    Serial.println(message);
  }
  
  if (data == "")
  {
    digitalWrite(13,LOW);
   // Serial.println("88.0,88.0,88.0,88.0,88.0,88.0");
  }
  else
  {
    // Serial.println(data);
    
  //  Serial.println(data);
  }
  
  delay(20);
}

