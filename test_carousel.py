
import hardware
import time

print("=== Testing Carousel Logic ===")
print(f"HAS_GPIO: {hardware.HAS_GPIO}")

# Mock initialization if needed (usually handled by app.py or hardware.init)
# hardware.setup_gpio() # This will return False on Windows

print("\n--- Testing Dispense Dose for Box 1 ---")
success, msg = hardware.dispense_dose(1)
print(f"Result: {success}")
print(f"Message: {msg}")

print("\n--- Testing Load Medicine ---")
hardware.load_medicine()
print("Load medicine command sent.")

print("\n--- Testing Go Zero ---")
hardware.go_home_zero()
print("Go Zero command sent.")
