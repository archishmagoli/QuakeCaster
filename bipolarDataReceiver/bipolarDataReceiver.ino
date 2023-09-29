#include "VernierLib.h" //include Vernier functions in this sketch

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
VernierLib Vernier; //create an instance of the VernierLib library

float sensorReading; //create global variable to store sensor reading

// Setup
void setup() {
  Serial.begin(9600);
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  Vernier.autoID(); // identify the sensor being used
}

void loop() {
  // Configure the Enable Pin to LOW when it needs to run
  digitalWrite(enPin,LOW);

  // Analyzing and parsing the data
  String motorSpecs = Serial.readStringUntil('\n');
  Parse_the_Data(motorSpecs);
  while (motorSpecs != "" && Serial.available() == 0) {
    Parse_the_Data(motorSpecs);
    if (motDirString == "Clockwise") {
      motor_Run_Clockwise(0.5 * motSpeedFloat);
    } else if (motDirString == "Anticlockwise") {
      motor_Run_Anticlockwise(0.5 * motSpeedFloat);
    } else if (motDirString == "Stop") {
      digitalWrite(enPin, HIGH);
      break;
    } else {
      Serial.println("Please enter valid input.");
      break;
    }
    if (Serial.available() > 0) {
      motorSpecs = Serial.readStringUntil('\n');
    }
  }
  readSensor();
}

void readSensor() {
  sensorReading = Vernier.readSensor(); // read one data value
  Serial.println(sensorReading); // graph data point 
  // delay(500); // wait half second
}

// Clockwise run function
void motor_Run_Clockwise(float delaySec) {
  digitalWrite(dirPin, LOW);
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(delaySec); 
  digitalWrite(stepPin,LOW); 
  delay(delaySec); 
  readSensor();
  delay(delaySec);
}

// Anticlockwise run function
void motor_Run_Anticlockwise(float delaySec) {
  digitalWrite(dirPin, HIGH);
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(delaySec); 
  digitalWrite(stepPin,LOW); 
  delay(delaySec); 
  readSensor();
  delay(delaySec);
}

long Parse_the_Data(String dataIn) {
  // Indexes separate input stream values
  indexA = dataIn.indexOf("A");
  indexB = dataIn.indexOf("B");
  indexC = dataIn.indexOf("D");

  // Extract data between separators
  motRun = dataIn.substring(0, indexA);
  motRunInt = motRun.toInt();
  motSpeed = dataIn.substring(indexA + 1, indexB);
  motSpeedFloat = motSpeed.toFloat();
  motDir = dataIn.substring(indexB + 1, indexC);
  motDirString = String(motDir);
}