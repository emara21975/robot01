#include <MPU6050_light.h>
#include <Wire.h>

MPU6050 mpu(Wire);

// ======= L298N Motor Driver ========
// Motor A (Left)
const int ENA = 5;
const int IN1 = 8;
const int IN2 = 9;

// Motor B (Right)
const int ENB = 6;
const int IN3 = 10;
const int IN4 = 11;

// ======= Ultrasonic Sensor ========
const int trigPin = 2;
const int echoPin = 3;

float distance;
long duration;

// -------- Robot State --------
enum RobotState { IDLE, MOVING };

RobotState state = IDLE;
bool isReversing = false;

float obstacleDistance = 20.0;

// -------- PID for straight line --------
float Kp = 3.0;
float Ki = 0.01;
float Kd = 1.5;

float errorSum = 0;
float lastError = 0;
float targetYaw = 0;

// -------- Speed --------
int currentSpeed = 0;
int targetSpeed = 150;
int speedStep = 5;

// ============ Normalize angle to -180 to 180 ============
float normalize(float angle) {
  while (angle > 180)
    angle -= 360;
  while (angle < -180)
    angle += 360;
  return angle;
}

// ============ Ultrasonic Distance ============
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 20000);
  return duration * 0.0343 / 2;
}

// ============ Motor Control ============
void stopRobot() {
  // Stop both motors
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void setMotorSpeed(int leftSpeed, int rightSpeed, bool forward) {
  // Set direction for Motor A (Left)
  if (forward) {
    digitalWrite(IN1, LOW);  // Inverted: Was HIGH
    digitalWrite(IN2, HIGH); // Inverted: Was LOW
  } else {
    digitalWrite(IN1, HIGH); // Inverted
    digitalWrite(IN2, LOW);  // Inverted
  }

  // Set direction for Motor B (Right)
  if (forward) {
    digitalWrite(IN3, LOW);  // Inverted: Was HIGH
    digitalWrite(IN4, HIGH); // Inverted: Was LOW
  } else {
    digitalWrite(IN3, HIGH); // Inverted
    digitalWrite(IN4, LOW);  // Inverted
  }

  // Set speed for both motors
  analogWrite(ENA, constrain(leftSpeed, 0, 255));
  analogWrite(ENB, constrain(rightSpeed, 0, 255));
}

void forwardPID(int baseSpeed) {
  // PID Disabled for debugging - Force straight movement
  setMotorSpeed(baseSpeed, baseSpeed, true);

  /*
  // Original PID Code (Disabled)
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  float error = normalize(yaw - targetYaw);

  errorSum += error;
  errorSum = constrain(errorSum, -1000, 1000);  // Prevent windup
  float derivative = error - lastError;
  lastError = error;

  float correction = Kp * error + Ki * errorSum + Kd * derivative;

  int leftSpeed = baseSpeed - correction;
  int rightSpeed = baseSpeed + correction;

  setMotorSpeed(leftSpeed, rightSpeed, true);
  */
}

void backwardPID(int baseSpeed) {
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  float error = normalize(yaw - targetYaw);

  errorSum += error;
  errorSum = constrain(errorSum, -1000, 1000); // Prevent windup
  float derivative = error - lastError;
  lastError = error;

  float correction = Kp * error + Ki * errorSum + Kd * derivative;

  // Reverse correction for backward
  int leftSpeed = baseSpeed + correction;
  int rightSpeed = baseSpeed - correction;

  setMotorSpeed(leftSpeed, rightSpeed, false);
}

// ============ Setup ============
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  // Motor pins - ALL as OUTPUT
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Ultrasonic pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initialize motors to stopped state
  stopRobot();

  // MPU6050 init
  Wire.begin();
  byte status = mpu.begin();

  delay(1000);
  mpu.calcOffsets();

  Serial.println("READY");
  Serial.println("Commands: START, STOP, RETURN");

  // Test both motors briefly
  Serial.println("Testing motors...");
  setMotorSpeed(100, 100, true);
  delay(500);
  stopRobot();
  Serial.println("Motor test complete");
}

// ============ Command Handler ============
void checkSerialCommands() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();

    if (command == "START" || command == "GO") {
      // Move forward
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      errorSum = 0;
      lastError = 0;
      currentSpeed = 0;
      state = MOVING;
      isReversing = false;
      Serial.println("OK:MOVING_FORWARD");

    } else if (command == "STOP") {
      state = IDLE;
      currentSpeed = 0;
      stopRobot();
      Serial.println("OK:STOPPED");

    } else if (command == "RETURN" || command == "REVERSE") {
      // Move backward
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      errorSum = 0;
      lastError = 0;
      currentSpeed = 0;
      state = MOVING;
      isReversing = true;
      Serial.println("OK:MOVING_BACKWARD");

    } else if (command == "TEST") {
      // Test both motors
      Serial.println("Testing Motor A (Left)...");
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 150);
      delay(1000);
      analogWrite(ENA, 0);

      Serial.println("Testing Motor B (Right)...");
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENB, 150);
      delay(1000);
      analogWrite(ENB, 0);

      stopRobot();
      Serial.println("OK:TEST_COMPLETE");

    } else {
      Serial.print("ERR:UNKNOWN_CMD:");
      Serial.println(command);
    }
  }
}

// ============ Main Loop ============
static unsigned long lastPrintTime = 0;

void loop() {
  checkSerialCommands();

  if (state == MOVING) {
    distance = getDistance();

    // Print distance every 200ms
    if (millis() - lastPrintTime >= 200) {
      lastPrintTime = millis();
      Serial.print("DISTANCE:");
      Serial.println(distance);
    }

    // Obstacle detection (only when moving forward)
    if (!isReversing && distance > 0 && distance <= obstacleDistance) {
      state = IDLE;
      stopRobot();
      currentSpeed = 0;
      Serial.println("OBSTACLE:STOPPED");
    } else {
      // Speed ramp up
      if (currentSpeed < targetSpeed) {
        currentSpeed += speedStep;
      }

      // Move with PID correction
      if (isReversing) {
        backwardPID(currentSpeed);
      } else {
        forwardPID(currentSpeed);
      }
    }
  } else {
    // IDLE state
    stopRobot();
  }

  delay(20);
}
