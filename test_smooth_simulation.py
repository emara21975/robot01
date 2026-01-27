import sys
import os
import time

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

import hardware

print("=== Testing Smooth Servo Movement (Simulation) ===")
print("Note: This test runs without actual hardware (GPIO).")
print("-" * 50)

# 1. Test direct smooth move call
print("\nTest 1: Direct Smooth Move (0 -> 90)")
hardware.smooth_move(None, 0, 90, steps=10)

# 2. Test Dispense Dose (Full Flow)
print("\nTest 2: Dispense Dose Flow (Box 1)")
# Box 1 is at 25 degrees
print("Expected behavior: Carousel moves 0 -> 25 (smooth), Gate opens (smooth), Gate closes (smooth), Carousel moves 25 -> 0 (smooth)")

success, msg = hardware.dispense_dose(1)
print(f"\nResult: {success}, Message: {msg}")

print("-" * 50)
print("=== Test Complete ===")
