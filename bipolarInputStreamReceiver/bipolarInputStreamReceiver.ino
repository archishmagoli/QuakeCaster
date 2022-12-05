// Defining the connecting ports
const int stepPin = 5; 
const int dirPin = 2; 
const int enPin = 8;
const int delaySec = 500;

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

    // Create a place to hold the incoming message
    static char motData[MAX_MESSAGE_LENGTH]; // Created an array of characters to hold the message
    static unsigned int index_pos = 0; // represents the index position as we traverse through motData[]

    // Read the next available byte in the serial receiver
    char charData = Serial.read();

    if (charData != '\n') 
    {
      motData[index_pos] = charData;
      Serial.print(motData[index_pos]);
      index_pos++;
    } 
    else 
    {
      motData[index_pos] = '\0'; // Indicates the end of the string
      index_pos = 0; // index_pos is reset
      Parse_the_Data(motData); // value is parsed

      // Serial.println(motRunInt);
      // Serial.println(motSpeedFloat);
      // Serial.println(motDirString);
      // Serial.println('\n');

      while (motDirString == "Clockwise") {
        
        motor_Run_Clockwise(motSpeedFloat);
      }
      while (motDirString == "Anticlockwise") {
        motor_Run_Anticlockwise(motSpeedFloat);
      }
    } 
  }
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
  motSpeedFloat = (10 - motSpeed.toFloat())*200;
  
  motDir = dataIn.substring(indexB + 1, indexC);
  motDirString = String(motDir);
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
