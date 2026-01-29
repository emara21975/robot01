#include <MPU6050_light.h>
#include <Wire.h>
#include <Servo.h>

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

// ======= DISPENSER HARDWARE (Allocated Pins) ========
// Assumption: Using free digital pins 4, 7, 12
Servo servoCarousel;
Servo gateServoA; // For Slot A
Servo gateServoB; // For Slot B

int PIN_CAROUSEL = 4;
int PIN_GATE_A = 7;
int PIN_GATE_B = 12;

// Dispenser Configuration
const int SLOT_A_ANGLE = 30;    // Calibrate this!
const int SLOT_B_ANGLE = 210;   // Calibrate this!
const int GATE_OPEN_ANGLE = 90;
const int GATE_CLOSE_ANGLE = 0;

// -------- Robot State --------
enum RobotState { IDLE, MOVING, TURNING, DISPENSING };

RobotState state = IDLE;
bool isReversing = false;

// Dispensing State Machine
enum DispenseStage { D_ROTATE, D_WAIT_ROTATE, D_OPEN, D_WAIT_USE, D_CLOSE, D_FINISH };
DispenseStage dispStage = D_ROTATE;
unsigned long dispTimer = 0;
unsigned long dispenseStartMs = 0; // Watchdog Timer
Servo* activeGateServo = NULL;
int targetCarouselAngle = 0;

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

// ============ Dispensing Logic (Safe Version) ============

// Safety Helper: Close all gates immediately
void closeAllGates() {
  if(!gateServoA.attached()) gateServoA.attach(PIN_GATE_A);
  if(!gateServoB.attached()) gateServoB.attach(PIN_GATE_B);
  
  gateServoA.write(GATE_CLOSE_ANGLE);
  gateServoB.write(GATE_CLOSE_ANGLE);
}

// Safety Helper: Abort operation and reset state
void abortDispense() {
  closeAllGates();
  servoCarousel.write(SLOT_A_ANGLE); // Reset carousel to safe known angle
  
  state = IDLE;
  dispStage = D_ROTATE;
  
  // Power down gates after abort
  delay(200);
  gateServoA.detach();
  gateServoB.detach();
  
  Serial.println("ERR:DISPENSE_ABORTED");
}

void startDispense(char slot) {
  if (state != IDLE) {
    Serial.println("ERR:BUSY");
    return;
  }
  
  // 1. Safety Close First
  closeAllGates(); 
  
  state = DISPENSING;
  dispStage = D_ROTATE;
  dispTimer = millis();
  dispenseStartMs = millis(); // Start Watchdog
  
  if (slot == 'A') {
    targetCarouselAngle = SLOT_A_ANGLE;
    activeGateServo = &gateServoA;
  } else {
    targetCarouselAngle = SLOT_B_ANGLE;
    activeGateServo = &gateServoB;
  }
  
  Serial.print("DISPENSE:START_");
  Serial.println(slot);
}

void updateDispenser() {
  unsigned long now = millis();
  
  // ⚠️ 4. Watchdog Timer (8 Seconds Timeout)
  if (now - dispenseStartMs > 8000) {
      Serial.println("ERR:WATCHDOG_TIMEOUT");
      abortDispense();
      return;
  }
  
  switch(dispStage) {
    case D_ROTATE:
      servoCarousel.write(targetCarouselAngle);
      dispTimer = now;
      dispStage = D_WAIT_ROTATE;
      break;
      
    case D_WAIT_ROTATE:
      if (now - dispTimer > 1000) { // Wait 1s for rotation
        dispStage = D_OPEN;
      }
      break;
      
    case D_OPEN:
      // Ensure specific servo is attached before move
      if (activeGateServo && !activeGateServo->attached()) {
          if (activeGateServo == &gateServoA) gateServoA.attach(PIN_GATE_A);
          else if (activeGateServo == &gateServoB) gateServoB.attach(PIN_GATE_B);
      }
      
      if(activeGateServo) activeGateServo->write(GATE_OPEN_ANGLE);
      dispTimer = now;
      dispStage = D_WAIT_USE;
      break;
      
    case D_WAIT_USE:
      if (now - dispTimer > 2000) { // Wait 2s for drops
        dispStage = D_CLOSE;
      }
      break;
      
    case D_CLOSE:
      if(activeGateServo) activeGateServo->write(GATE_CLOSE_ANGLE);
      
      // ⚠️ 3. REMOVED Auto-Home to prevent risk
      // servoCarousel.write(SLOT_A_ANGLE); 
      
      dispTimer = now;
      dispStage = D_FINISH;
      break;
      
    case D_FINISH:
      if (now - dispTimer > 500) {
        state = IDLE;
        
        // ⚠️ 2. Detach to save power/heat
        gateServoA.detach();
        gateServoB.detach();
        
        Serial.println("STATUS:DISPENSE_COMPLETE");
      }
      break;
  }
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
  
  // Servos
  servoCarousel.attach(PIN_CAROUSEL);
  gateServoA.attach(PIN_GATE_A);
  gateServoB.attach(PIN_GATE_B);
  
  // Home Servos
  servoCarousel.write(SLOT_A_ANGLE);
  gateServoA.write(GATE_CLOSE_ANGLE);
  gateServoB.write(GATE_CLOSE_ANGLE);
  
  // Stabilize and Detach Gates
  delay(1000);
  gateServoA.detach();
  gateServoB.detach();

  Wire.begin();
  
  // MPU Init Safety Check
  byte status = mpu.begin();
  if(status != 0){ } // Could add error LED here
  
  delay(1000);
  mpu.calcOffsets();

  Serial.println("READY");
}

// ============ Command Handler ============
void checkSerialCommands() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read until newline
    command.trim();
    command.toUpperCase();

    // Serial.print("CMD="); Serial.println(command);

    if (command == "START" || command == "GO") {
      mpu.update();
      targetYaw = normalize(mpu.getAngleZ());
      state = MOVING;
      isReversing = false;
      Serial.println("OK:MOVING_FWD");

    } else if (command == "STOP") {
      // ⚠️ 1. Safety Halt
      abortDispense();
      
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
      
    } else if (command == "DISPENSE A") {
      startDispense('A');
      
    } else if (command == "DISPENSE B") {
      startDispense('B');
    }
  }
}

// ============ Main Loop ============
static unsigned long lastPrintTime = 0;

void loop() {
  checkSerialCommands();

  if (state == DISPENSING) {
    updateDispenser();
    
  } else if (state == TURNING) {
    turnInPlace();
    
  } else if (state == MOVING) {
    distance = getDistance();

    if (millis() - lastPrintTime >= 200) {
      lastPrintTime = millis();
      Serial.print("DISTANCE:");
      Serial.println(distance);
    }

    // Safety Stop
    if (distance > 0 && distance <= obstacleDistance) {
      // ⚠️ 1. Safety Halt on Obstacle
      abortDispense();
      
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
