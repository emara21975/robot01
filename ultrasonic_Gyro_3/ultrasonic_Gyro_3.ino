#include <MPU6050_light.h>
#include <Wire.h>

MPU6050 mpu(Wire);

// ======= L298N ========
int ENA = 5;
int IN1 = 8;
int IN2 = 9;

int ENB = 6;
int IN3 = 10;
int IN4 = 11;

// ======= Ultrasonic ========
int trigPin = 2;
int echoPin = 3;

float distance;
long duration;

// -------- Robot State --------
// NOTE: DISPENSING state removed - now handled by Raspberry Pi GPIO
enum RobotState { IDLE, MOVING, TURNING };

RobotState state = IDLE;
bool isReversing = false;

float obstacleDistance = 20.0;

// -------- PID --------
float Kp = 3.0;
float Ki = 0.01;
float Kd = 1.5;

float errorSum = 0;
float lastError = 0;

// -------- Speed Ramp --------
int currentSpeed = 0;
int targetSpeed = 150;
int speedStep = 5;

// -------- Targets --------
float targetYaw = 0;
float turnTargetYaw = 0;
unsigned long turnStartMs = 0;

// ============ Normalize ============
float normalize(float angle) {
  while (angle > 180)
    angle -= 360;
  while (angle < -180)
    angle += 360;
  return angle;
}

// ============ Ultrasonic ============
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

  // Reverse correction logic (inverted steering)
  int L = constrain(baseSpeed + correction, 0, 255);
  int R = constrain(baseSpeed - correction, 0, 255);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, L);
  analogWrite(ENB, R);
}

// ============ Turn In Place Logic ============
void startTurnDegrees(float deltaDeg) {
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  turnTargetYaw = normalize(yaw + deltaDeg);

  errorSum = 0;
  lastError = 0;
  turnStartMs = millis();

  state = TURNING;
  currentSpeed = 0;

  Serial.print("TURN_DEG:");
  Serial.println(deltaDeg);
  Serial.print("FROM:");
  Serial.println(yaw);
  Serial.print("TARGET:");
  Serial.println(turnTargetYaw);
}

void turnInPlace() {
  mpu.update();
  float yaw = normalize(mpu.getAngleZ());
  float error = normalize(turnTargetYaw - yaw);

  // Threshold to stop turning (3 degrees)
  if (abs(error) < 3) {
    stopRobot();
    delay(500);

    // Default behavior: Go IDLE after turn
    state = IDLE;
    Serial.println("STATUS:TURN_COMPLETE");
    return;
  }

  int turnSpeed = 100; // Fixed turn speed

  if (error > 0) {
    // Turn Right (CW)
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  } else {
    // Turn Left (CCW)
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  }

  analogWrite(ENA, turnSpeed);
  analogWrite(ENB, turnSpeed);
}


// ============ Setup ============
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Wire.begin();
  
  // MPU Init Safety Check
  byte status = mpu.begin();
  if(status != 0){ } // Could add error LED here
  
  delay(1000);
  mpu.calcOffsets();

  Serial.println("READY");
  Serial.println("NOTE: Dispenser control moved to Raspberry Pi GPIO");
}

// ============ Command Handler ============
void checkSerialCommands() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read until newline
    command.trim();
    command.toUpperCase();

    if (command == "START" || command == "GO") {
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      state = MOVING;
      isReversing = false;
      Serial.println("OK:MOVING_FWD");

    } else if (command == "STOP") {
      state = IDLE;
      stopRobot();
      Serial.println("OK:STOPPED");

    } else if (command == "RIGHT") {
      startTurnDegrees(90);
      Serial.println("OK:TURN_RIGHT");

    } else if (command == "LEFT") {
      startTurnDegrees(-90);
      Serial.println("OK:TURN_LEFT");

    } else if (command == "REVERSE") {
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      state = MOVING;
      isReversing = true;
      Serial.println("OK:RAW_REVERSE");

    } else if (command == "RETURN") {
      // Chain: Turn 180 -> Wait for next command (or User sends Start)
      startTurnDegrees(180);
      Serial.println("OK:STARTING_RETURN");
      
    // DISPENSE commands removed - handled by Raspberry Pi GPIO now
    } else if (command == "DISPENSE A" || command == "DISPENSE B" || 
               command.startsWith("CAROUSEL ") || 
               command.startsWith("GATE A ") || 
               command.startsWith("GATE B ")) {
      Serial.println("ERR:DISPENSE_MOVED_TO_PI");
      Serial.println("NOTE: Dispensing is now controlled by Raspberry Pi GPIO");
    }
  }
}

// ============ Main Loop ============
static unsigned long lastPrintTime = 0;

void loop() {
  checkSerialCommands();

  if (state == TURNING) {
    turnInPlace();
    
  } else if (state == MOVING) {
    distance = getDistance();

    if (millis() - lastPrintTime >= 200) {
      lastPrintTime = millis();
      Serial.print("DISTANCE:");
      Serial.println(distance);
    }

    // Safety Stop on Obstacle
    if (distance > 0 && distance <= obstacleDistance) {
      state = IDLE;
      stopRobot();
      currentSpeed = 0;
      Serial.println("OBSTACLE:STOPPED");
    } else {
      if (currentSpeed < targetSpeed)
        currentSpeed += speedStep;

      if (isReversing)
        backwardPID(currentSpeed);
      else
        forwardPID(currentSpeed);
    }
  } else {
    stopRobot();
  }

  delay(20); // Slightly faster loop
}
