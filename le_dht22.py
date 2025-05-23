import ASUS.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)  # ou GPIO.ASUS

GPIO.setup(7, GPIO.OUT)

try:
    while True:
        GPIO.output(7, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(7, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
