// Defining the connecting ports
const int stepPin = 5; 
const int dirPin = 2; 
const int enPin = 8;

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
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    if (input != "Stop") {
      if (input == "Clockwise") {
        motor_Run_Clockwise(500);
      } else if (input == "Anticlockwise") {
        motor_Run_Anticlockwise(500);
      }
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
  digitalWrite(dirPin, HIGH);
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(delaySec); 
  digitalWrite(stepPin,LOW); 
  delayMicroseconds(delaySec); 
}
