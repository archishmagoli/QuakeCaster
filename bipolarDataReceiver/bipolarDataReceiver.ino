#include "VernierLib.h" // include Vernier functions in this sketch

// Defining the connecting ports
const int stepPin = 5;
const int dirPin = 2;
const int enPin = 8;

// Converted final variables, used to run the motor
int motRunInt;
float motSpeedFloat;
String motDirString;
VernierLib Vernier; // create an instance of the VernierLib library

float sensorReading; // create a global variable to store sensor reading
unsigned long previousSensorReadMillis = 0;
const unsigned long sensorReadIntervalMillis = 1000; // Time in milliseconds for sensor reading

// Motor control variables
unsigned long previousMotorStepMillis = 0;
float motorStepInterval = 0;

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
  // Check for new commands
  if (Serial.available() > 0) {
    String motorSpecs = Serial.readStringUntil('\n');
    Parse_the_Data(motorSpecs);

    if (motDirString == "Clockwise") {
      motorStepInterval = 0.5 * motSpeedFloat;
      digitalWrite(dirPin, LOW);
      digitalWrite(enPin, LOW); // Enable the motor
    } else if (motDirString == "Anticlockwise") {
      motorStepInterval = 0.5 * motSpeedFloat;
      digitalWrite(dirPin, HIGH);
      digitalWrite(enPin, LOW); // Enable the motor
    } else if (motDirString == "Stop") {
      digitalWrite(enPin, HIGH); // Disable the motor
      motorStepInterval = 0; // Stop stepping
    }
  }

  // Update the motor steps based on the interval
  unsigned long currentMillis = millis();
  if (currentMillis - previousMotorStepMillis >= motorStepInterval && (motDirString == "Clockwise" || motDirString == "Anticlockwise")) {
    stepMotor();
    previousMotorStepMillis = currentMillis;
  }

  // Read the sensor data every second
  if (currentMillis - previousSensorReadMillis >= sensorReadIntervalMillis) {
    readSensor();
    previousSensorReadMillis = currentMillis;
  }
}

void readSensor() {
  sensorReading = Vernier.readSensor(); // read one data value
  Serial.println(sensorReading); // graph data point
}

void stepMotor() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(200); // Adjust this delay as needed for your motor
  digitalWrite(stepPin, LOW);
  delayMicroseconds(200); // Adjust this delay as needed for your motor
}

void Parse_the_Data(String dataIn) {
  // Indexes separate input stream values
  int indexA = dataIn.indexOf("A");
  int indexB = dataIn.indexOf("B");
  int indexC = dataIn.indexOf("D");

  // Extract data between separators
  String motRun = dataIn.substring(0, indexA);
  motRunInt = motRun.toInt();
  String motSpeed = dataIn.substring(indexA + 1, indexB);
  motSpeedFloat = motSpeed.toFloat();
  String motDir = dataIn.substring(indexB + 1, indexC);
  motDirString = String(motDir);
}
