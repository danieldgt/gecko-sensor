import ASUS.GPIO as GPIO
import time
import threading
import display

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pinos
DHT_PIN = 7
DHT_PIN2 = 8
LED_PINS = {
    'Azul': 11,
    'Verde': 13,
    'Vermelho': 15,
    'Amarelo': 16
}

# Setup dos LEDs
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def read_dht22(pin):
    data = []
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)
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
        return None

    humidity = humidity_raw / 10.0
    if temperature_raw & 0x8000:
        temperature_raw = -(temperature_raw & 0x7FFF)
    temperature = temperature_raw / 10.0
    return temperature, humidity

def thread_leds():
    def piscar():
        ordem = ['Amarelo', 'Azul', 'Vermelho', 'Verde', 'Vermelho', 'Azul', 'Amarelo']
        while True:
            for cor in ordem:
                for c, pin in LED_PINS.items():
                    GPIO.output(pin, GPIO.HIGH if c == cor else GPIO.LOW)
                time.sleep(0.2)
    return threading.Thread(target=piscar, daemon=True)

def thread_sensores():
    def ler():
        while True:
            result = read_dht22(DHT_PIN)
            result2 = read_dht22(DHT_PIN2)
            temp1, hum1 = result if result else (0.0, 0.0)
            temp2, hum2 = result2 if result2 else (0.0, 0.0)

            display.atualizar_temperatura_umidade(temp1, hum1, temp2, hum2)

            GPIO.setup(DHT_PIN, GPIO.OUT)
            GPIO.output(DHT_PIN, GPIO.HIGH)
            GPIO.setup(DHT_PIN2, GPIO.OUT)
            GPIO.output(DHT_PIN2, GPIO.HIGH)

            time.sleep(4)
    return threading.Thread(target=ler, daemon=True)
