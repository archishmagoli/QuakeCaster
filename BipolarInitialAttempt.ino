const int stepPin = 3; 
const int dirPin = 4; 
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
}
void loop() {
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(1500); 
  digitalWrite(stepPin,LOW); 
  delayMicroseconds(1500);
}