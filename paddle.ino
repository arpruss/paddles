void setup() {
  // put your setup code here, to run once:
  Serial.begin(230400);  
  pinMode(0, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
}

char hexNibble(uint8_t x) {
  return x < 10 ? x+'0' : x+('A'-10);
}

void loop() {
  Serial.write(':');
  Serial.write('0'+digitalRead(0));
  Serial.write('1'+digitalRead(1));
  for (int i=0; i<2; i++) {
    uint8_t d = analogRead(i) >> 3;
    Serial.write(hexNibble(d>>4));
    Serial.write(hexNibble(d&0xF));
  }
  delay(5);
}

