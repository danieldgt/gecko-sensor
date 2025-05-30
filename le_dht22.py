import ASUS.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pinos dos sensores
DHT_PIN = 7   # Pino físico 7 (GPIO 4)
DHT_PIN2 = 8  # Pino físico 8 (GPIO 14)

# Pinos dos LEDs
LED_PINS = {
    'Azul': 11,     # GPIO 17
    'Verde': 13,    # GPIO 27
    'Vermelho': 15, # GPIO 22
    'Amarelo': 16   # GPIO 23
}

# Inicializa os pinos dos LEDs
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
        print("Checksum inválido")
        return None

    humidity = humidity_raw / 10.0

    if temperature_raw & 0x8000:
        temperature_raw = -(temperature_raw & 0x7FFF)
    temperature = temperature_raw / 10.0

    return temperature, humidity

# Thread para piscar LEDs na sequência especificada
def piscar_leds_sequencia():
    ordem = ['Amarelo', 'Azul', 'Vermelho', 'Verde', 'Vermelho', 'Azul', 'Amarelo']
    while True:
        for cor in ordem:
            for c, pin in LED_PINS.items():
                GPIO.output(pin, GPIO.HIGH if c == cor else GPIO.LOW)
            time.sleep(1)

# Thread para ler sensores
def ler_sensores():
    try:
        while True:
            result = read_dht22(DHT_PIN)
            result2 = read_dht22(DHT_PIN2)
            if result:
                temp, hum = result
                print("1 - Temperatura: {}°C, Umidade: {}%".format(temp, hum))
            else:
                print("Falha ao ler o sensor 1")

            if result2:
                temp2, hum2 = result2
                print("2 - Temperatura: {}°C, Umidade: {}%".format(temp2, hum2))
            else:
                print("Falha ao ler o sensor 2")

            # Reset dos pinos dos sensores
            GPIO.setup(DHT_PIN, GPIO.OUT)
            GPIO.output(DHT_PIN, GPIO.HIGH)
            GPIO.setup(DHT_PIN2, GPIO.OUT)
            GPIO.output(DHT_PIN2, GPIO.HIGH)

            time.sleep(4)
    except KeyboardInterrupt:
        GPIO.cleanup()

# Inicia threads separadas
t1 = threading.Thread(target=piscar_leds_sequencia, daemon=True)
t2 = threading.Thread(target=ler_sensores)

t1.start()
t2.start()

t2.join()
