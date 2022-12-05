// Defining the connecting ports
const int stepPin = 5; 
const int dirPin = 2; 
const int enPin = 8;
// const int delaySec = 500;

// defining the temporary variables
const unsigned int MAX_MESSAGE_LENGTH = 50; // arbitrary number

// Parsing variables to capture the parameters
int8_t indexA, indexB, indexC;
String motDir, motRun, motSpeed;

// Converted final variables, used to run the motor
int motRunInt;
float motSpeedFloat;
String motDirString;

void setup() {
  Serial.begin(9600);

  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
}

void loop() {  
  // Check to see if anything is available in the Serial (input stream)
  while (Serial.available() > 0) {
    char charData = Serial.read();

    Serial.println(charData);

    while (charData == '5') {
      motor_Run_Clockwise(1000);
    }
  }
}

void motor_Run_Clockwise(float delaySec) {
    digitalWrite(dirPin, LOW);
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(delaySec); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(delaySec); 
}

void motor_Run_Anticlockwise(float delaySec) {
  Serial.println(delaySec);

  digitalWrite(dirPin, HIGH);
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(delaySec); 
  digitalWrite(stepPin,LOW); 
  delayMicroseconds(delaySec); 
}
