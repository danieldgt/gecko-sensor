import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DHT_PIN = 7  # Pino físico 7 (GPIO 4)

def read_dht22(pin):
    data = []

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20ms LOW start
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN)

    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.HIGH:
        if time.time() > timeout: return None
    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.LOW:
        if time.time() > timeout: return None
    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.HIGH:
        if time.time() > timeout: return None

    for i in range(40):
        timeout = time.time() + 0.1
        while GPIO.input(pin) == GPIO.LOW:
            if time.time() > timeout: return None
        t_start = time.time()
        timeout = time.time() + 0.1
        while GPIO.input(pin) == GPIO.HIGH:
            if time.time() > timeout: return None
        t_end = time.time()

        pulse_len = (t_end - t_start) * 1000000
        data.append(1 if pulse_len > 50 else 0)

    bytes_data = []
    for i in range(0, 40, 8):
        byte = 0
        for bit in data[i:i+8]:
            byte = (byte << 1) | bit
        bytes_data.append(byte)

    humidity_raw = (bytes_data[0] << 8) + bytes_data[1]
    temperature_raw = (bytes_data[2] << 8) + bytes_data[3]
    checksum = bytes_data[4]

    if ((sum(bytes_data[:4])) & 0xFF) != checksum:
        print("Checksum inválido")
        return None

    humidity = humidity_raw / 10.0

    if temperature_raw & 0x8000:
        temperature_raw = -(temperature_raw & 0x7FFF)
    temperature = temperature_raw / 10.0

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

    return temperature, humidity


# Leitura em loop com recuperação entre ciclos
try:
    while True:
        result = read_dht22(DHT_PIN)
        if result:
            temp, hum = result
            print("Temperatura: {}°C, Umidade: {}%".format(temp, hum))
        else:
            print("Falha ao ler o sensor")

        # Limpa estado do pino após cada leitura
        GPIO.setup(DHT_PIN, GPIO.OUT)
        GPIO.output(DHT_PIN, GPIO.HIGH)
        time.sleep(3)  # intervalo mínimo entre leituras

except KeyboardInterrupt:
    GPIO.cleanup()
