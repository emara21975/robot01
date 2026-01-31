#include <MPU6050_light.h>
#include <Wire.h>

MPU6050 mpu(Wire);

// ======= L298N Motor Driver ========
int ENA = 5;
int IN1 = 8;
int IN2 = 9;

int ENB = 6;
int IN3 = 10;
int IN4 = 11;

// ======= Ultrasonic Sensor ========
int trigPin = 2;
int echoPin = 3;

float distance;
long duration;

// -------- Robot State --------
// Simple: IDLE or MOVING (forward/backward)
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

// -------- Speed Ramp --------
int currentSpeed = 0;
int targetSpeed = 150;
int speedStep = 5;

// ============ Normalize angle to -180 to 180 ============
float normalize(float angle) {
  while (angle > 180) angle -= 360;
  while (angle < -180) angle += 360;
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
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void forwardPID(int baseSpeed) {
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  float error = normalize(yaw - targetYaw);

  errorSum += error;
  float derivative = error - lastError;
  lastError = error;

  float correction = Kp * error + Ki * errorSum + Kd * derivative;

  int L = constrain(baseSpeed - correction, 0, 255);
  int R = constrain(baseSpeed + correction, 0, 255);

  // Forward direction
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, L);
  analogWrite(ENB, R);
}

void backwardPID(int baseSpeed) {
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  float error = normalize(yaw - targetYaw);

  errorSum += error;
  float derivative = error - lastError;
  lastError = error;

  float correction = Kp * error + Ki * errorSum + Kd * derivative;

  // Reverse correction for backward
  int L = constrain(baseSpeed + correction, 0, 255);
  int R = constrain(baseSpeed - correction, 0, 255);

  // Backward direction
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, L);
  analogWrite(ENB, R);
}


// ============ Setup ============
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  // Motor pins
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Ultrasonic pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // MPU6050 init
  Wire.begin();
  byte status = mpu.begin();
  
  delay(1000);
  mpu.calcOffsets();

  Serial.println("READY");
  Serial.println("Commands: START, STOP, RETURN");
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
