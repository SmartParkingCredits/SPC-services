#include <Servo.h>

Servo myServo;  // Create servo object

void setup() {
  Serial.begin(9600);         // Start serial communication at 9600 baud rate
  myServo.attach(9);          // Attach the servo on pin 9 to the servo object
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming JSON string
    String jsonData = Serial.readStringUntil('\n');

    // Extract the position value from the JSON string
    int startPos = jsonData.indexOf(":") + 1;
    int endPos = jsonData.indexOf("}");
    String positionStr = jsonData.substring(startPos, endPos);
    int position = positionStr.toInt();  // Convert position to integer

    // Control the servo
    myServo.write(position);  // Move servo to the specified position

    // For debugging, print the position to the Serial Monitor
    Serial.print("Moving servo to position: ");
    Serial.println(position);
  }
}
