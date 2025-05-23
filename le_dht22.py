import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DHT_PIN = 7  # Pino físico 7 (GPIO 4)

def read_dht22(pin):
    data = []

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.05)  # estabiliza o sensor

    # Inicia comunicação
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20ms
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN)

    # Aguarda resposta do sensor (com timeout)
    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.HIGH:
        if time.time() > timeout:
            print("Timeout inicial (HIGH)")
            return None

    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.LOW:
        if time.time() > timeout:
            print("Timeout inicial (LOW)")
            return None

    timeout = time.time() + 0.1
    while GPIO.input(pin) == GPIO.HIGH:
        if time.time() > timeout:
            print("Timeout inicial (HIGH após LOW)")
            return None

    # Lê 40 bits com timeout
    for i in range(40):
        timeout = time.time() + 0.1
        while GPIO.input(pin) == GPIO.LOW:
            if time.time() > timeout:
                print("Timeout durante bit LOW")
                return None

        t_start = time.time()

        timeout = time.time() + 0.1
        while GPIO.input(pin) == GPIO.HIGH:
            if time.time() > timeout:
                print("Timeout durante bit HIGH")
                return None

        t_end = time.time()

        pulse_len = (t_end - t_start) * 1000000  # microssegundos
        data.append(1 if pulse_len > 50 else 0)

    # Converte bits em bytes
    bytes_data = []
    for i in range(0, 40, 8):
        byte = 0
        for bit in data[i:i+8]:
            byte = (byte << 1) | bit
        bytes_data.append(byte)

    humidity_int, humidity_dec, temperature_int, temperature_dec, checksum = bytes_data

    if ((humidity_int + humidity_dec + temperature_int + temperature_dec) & 0xFF) != checksum:
        print("Leitura inválida (checksum)")
        return None

    temperature = temperature_int + temperature_dec / 10.0
    humidity = humidity_int + humidity_dec / 10.0

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
        time.sleep(2)  # intervalo mínimo entre leituras

except KeyboardInterrupt:
    GPIO.cleanup()
