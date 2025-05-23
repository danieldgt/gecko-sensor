import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DHT_PIN = 7  # Pino físico 7 (GPIO 4)

def pulse_time():
    GPIO.setup(DHT_PIN, GPIO.OUT)
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.02)  # 20ms de sinal baixo para iniciar
    GPIO.output(DHT_PIN, GPIO.HIGH)
    GPIO.setup(DHT_PIN, GPIO.IN)

    print("Esperando resposta do sensor...")

    # Espera pull down
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        pass

    # Espera pull up
    while GPIO.input(DHT_PIN) == GPIO.LOW:
        pass

    # Espera fim do sinal de resposta
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        pass

    print("Lendo pulsos:")

    timings = []
    for i in range(40):
        # LOW
        while GPIO.input(DHT_PIN) == GPIO.LOW:
            pass

        t_start = time.time()

        # HIGH
        while GPIO.input(DHT_PIN) == GPIO.HIGH:
            pass

        t_end = time.time()

        pulse_len = (t_end - t_start) * 1_000_000  # microssegundos
        timings.append(pulse_len)

    return timings

try:
    while True:
        pulses = pulse_time()
        print("Pulsos (µs):")
        for i, p in enumerate(pulses):
            print("Bit {}: {:.1f} µs".format(i+1, p))
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
