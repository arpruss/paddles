void setup() {
  // put your setup code here, to run once:
  Serial.begin(230400);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  int datum = analogRead(0);
  Serial.println(String("L")+datum);
  datum = analogRead(1);
  Serial.println(String("R")+datum);
}

