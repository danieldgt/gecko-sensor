import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DHT_PIN = 7  # Pino físico 7 (GPIO 4)

def read_dht22(pin):
    data = []

    # Sinal de início para o sensor
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20ms
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN)

    # Aguarda resposta do sensor
    while GPIO.input(pin) == GPIO.HIGH:
        pass
    while GPIO.input(pin) == GPIO.LOW:
        pass
    while GPIO.input(pin) == GPIO.HIGH:
        pass

    # Lê 40 bits
    for i in range(40):
        while GPIO.input(pin) == GPIO.LOW:
            pass

        t_start = time.time()

        while GPIO.input(pin) == GPIO.HIGH:
            pass

        t_end = time.time()

        pulse_len = (t_end - t_start) * 1000000  # microssegundos
        data.append(1 if pulse_len > 50 else 0)

    # Converte os bits para bytes
    bytes_data = []
    for i in range(0, 40, 8):
        byte = 0
        for bit in data[i:i+8]:
            byte = (byte << 1) | bit
        bytes_data.append(byte)

    humidity_int = bytes_data[0]
    humidity_dec = bytes_data[1]
    temperature_int = bytes_data[2]
    temperature_dec = bytes_data[3]
    checksum = bytes_data[4]

    if ((humidity_int + humidity_dec + temperature_int + temperature_dec) & 0xFF) != checksum:
        print("Leitura inválida (checksum)")
        return None

    temperature = temperature_int + temperature_dec / 10.0
    humidity = humidity_int + humidity_dec / 10.0

    return temperature, humidity

# Leitura de teste
try:
    while True:
        result = read_dht22(DHT_PIN)
        if result:
            temp, hum = result
            print("Temperatura: {}°C, Umidade: {}%".format(temp, hum))
        else:
            print("Falha ao ler o sensor")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
