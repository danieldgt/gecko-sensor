import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

PIN = 7  # Físico 7 = GPIO 4

GPIO.setup(PIN, GPIO.IN)

print("Monitorando mudanças no pino por 5 segundos...")

start_time = time.time()
while time.time() - start_time < 5:
    val = GPIO.input(PIN)
    print("GPIO está: {}".format(val))
    time.sleep(0.05)
