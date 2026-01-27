import threading
import time

class RobotState:
    IDLE = "IDLE"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    DISPENSING = "DISPENSING"
    ERROR = "ERROR"

class StateMachine:
    def __init__(self):
        self._state = RobotState.IDLE
        self._lock = threading.Lock()
        self._verified_time = 0
        self._verified_timeout = 60 # Seconds to stay verified before reset

    @property
    def current(self):
        """Get current state safely"""
        with self._lock:
            # Auto-expired verification
            if self._state == RobotState.VERIFIED:
                 if (time.time() - self._verified_time) > self._verified_timeout:
                     print("⏳ Verification Expired. Resetting to IDLE.")
                     self._state = RobotState.IDLE
            return self._state

    def set(self, new_state):
        """Transition to new state safely"""
        with self._lock:
            print(f"🔄 State Transition: {self._state} -> {new_state}")
            self._state = new_state
            if new_state == RobotState.VERIFIED:
                self._verified_time = time.time()

    def can_verify(self):
        """Check if we can start verification"""
        return self.current in [RobotState.IDLE, RobotState.VERIFIED]

    def can_dispense(self):
        """Check if we can dispense (Must be VERIFIED or auth disabled)"""
        return self.current == RobotState.VERIFIED

    def is_busy(self):
        """Check if robot is doing critical work"""
        return self.current in [RobotState.VERIFYING, RobotState.DISPENSING]

# Singleton Instance
robot_state = StateMachine()
