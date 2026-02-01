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

// -------- Robot State Machine --------
enum RobotState { IDLE, FORWARD, BACKWARD };
RobotState state = IDLE;

float obstacleDistance = 20.0;

// -------- PID for straight line (Currently Disabled logic) --------
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

// -------- Safety --------
unsigned long lastCommandTime = 0;
const unsigned long SAFETY_TIMEOUT = 3000; // 3 Seconds

// ============ Normalize angle to -180 to 180 ============
float normalize(float angle) {
  while (angle > 180)
    angle -= 360;
  while (angle < -180)
    angle += 360;
  return angle;
}

// ============ Ultrasonic Distance (Filtered) ============
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 20000); // 20ms timeout

  if (duration == 0)
    return 999.0; // Timeout

  float dist = duration * 0.0343 / 2;

  // Basic Filter: Ignore impossible values
  if (dist <= 0 || dist > 400)
    return 999.0;

  return dist;
}

// ============ Motor Control ============

void stopCoast() {
  // Coast Stop (Free wheel)
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void stopBrake() {
  // Hard Brake (Short circuit motors)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 255); // Maximum force for braking
  analogWrite(ENB, 255);
  delay(100);  // Hold brake briefly
  stopCoast(); // Then relax
}

void setMotorSpeed(int leftSpeed, int rightSpeed, bool forward) {
  // Set direction for Motor A (Left)
  if (forward) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }

  // Set direction for Motor B (Right)
  if (forward) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }

  // Set speed for both motors
  analogWrite(ENA, constrain(leftSpeed, 0, 255));
  analogWrite(ENB, constrain(rightSpeed, 0, 255));
}

void forwardPID(int baseSpeed) {
  // Forced straight movement (PID disabled)
  setMotorSpeed(baseSpeed, baseSpeed, true);
}

void backwardPID(int baseSpeed) {
  // Forced straight backward movement (PID disabled)
  setMotorSpeed(baseSpeed, baseSpeed, false);
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

  stopCoast();

  // MPU6050 init
  Wire.begin();
  byte status = mpu.begin();

  delay(1000);
  mpu.calcOffsets();

  Serial.println("READY");
  Serial.println("Commands: START, STOP, RETURN");

  lastCommandTime = millis();
}

// ============ Command Handler ============
void checkSerialCommands() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();

    lastCommandTime = millis(); // Update heartbeat

    if (command == "START" || command == "GO") {
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      currentSpeed = 0;
      state = FORWARD;
      Serial.println("OK:MOVING_FORWARD");

    } else if (command == "STOP") {
      state = IDLE;
      currentSpeed = 0;
      stopBrake();
      Serial.println("OK:STOPPED");
      Serial.println("STATUS:IDLE");

    } else if (command == "RETURN" || command == "REVERSE") {
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      currentSpeed = 0;
      state = BACKWARD;
      Serial.println("OK:MOVING_BACKWARD");

    } else if (command == "TEST") {
      Serial.println("Testing Motors...");
      setMotorSpeed(150, 150, true);
      delay(1000);
      stopBrake();
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

  // Safety Timeout
  if (state != IDLE && (millis() - lastCommandTime > SAFETY_TIMEOUT)) {
    state = IDLE;
    stopBrake();
    Serial.println("ERR:SAFETY_TIMEOUT");
  }

  if (state == FORWARD || state == BACKWARD) {
    distance = getDistance();

    // Print distance
    if (millis() - lastPrintTime >= 200) {
      lastPrintTime = millis();
      Serial.print("DISTANCE:");
      Serial.println(distance);
    }

    // Obstacle Check (Only in FORWARD)
    if (state == FORWARD && distance > 0 && distance <= obstacleDistance) {
      state = IDLE;
      stopBrake();
      currentSpeed = 0;
      Serial.println("OBSTACLE:STOPPED");
    } else {
      // Speed ramp
      if (currentSpeed < targetSpeed) {
        currentSpeed += speedStep;
      }

      // Movement
      if (state == BACKWARD) {
        backwardPID(currentSpeed);
      } else {
        forwardPID(currentSpeed);
      }
    }
  } else {
    // IDLE
    stopCoast();
  }

  delay(20);
}
