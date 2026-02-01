
import RPi.GPIO as GPIO
import time

GATE_PIN = 23

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(GATE_PIN, GPIO.OUT)
pwm = GPIO.PWM(GATE_PIN, 50)
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(GATE_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(GATE_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    print(f"Testing Gate on Pin {GATE_PIN}")
    while True:
        cmd = input("Enter (o)pen, (c)lose, or (q)uit: ")
        if cmd == 'o':
            print("Opening (90)...")
            set_angle(90)
        elif cmd == 'c':
            print("Closing (0)...")
            set_angle(0)
        elif cmd == 'q':
            break
finally:
    pwm.stop()
    GPIO.cleanup()
