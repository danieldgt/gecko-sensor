import display
import ASUS.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# === CONFIGURACAO DE PINOS ===
DHT_PIN = 7
DHT_PIN2 = 8
LED_PINS = {
    'Azul': 11,     # GPIO 17
    'Verde': 13,    # GPIO 27
    'Vermelho': 15, # GPIO 22
    'Amarelo': 16   # GPIO 23
}

for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# === SENSOR DHT22 ===
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

# === CLASSE DE FILTRO ===
class SensorFiltro:
    def __init__(self, max_len=5, tolerancia=5.0):
        self.temperaturas = []
        self.umidades = []
        self.max_len = max_len
        self.tolerancia = tolerancia

    def filtrar(self, nova_temp, nova_umid):
        if nova_temp == 0.0 or nova_umid == 0.0:
            return None

        if not self.temperaturas:
            self._add(nova_temp, nova_umid)
            return nova_temp, nova_umid

        media_temp = sum(self.temperaturas) / len(self.temperaturas)
        media_umid = sum(self.umidades) / len(self.umidades)

        if (abs(nova_temp - media_temp) > self.tolerancia or
            abs(nova_umid - media_umid) > self.tolerancia):
            return None

        self._add(nova_temp, nova_umid)
        return nova_temp, nova_umid

    def _add(self, temp, umid):
        self.temperaturas.append(temp)
        self.umidades.append(umid)
        if len(self.temperaturas) > self.max_len:
            self.temperaturas.pop(0)
            self.umidades.pop(0)

# === THREAD SENSORES ===
def thread_sensores():
    def ler():
        filtro1 = SensorFiltro()
        filtro2 = SensorFiltro()
        while True:
            r1 = read_dht22(DHT_PIN)
            r2 = read_dht22(DHT_PIN2)
            f1 = filtro1.filtrar(*r1) if r1 else None
            f2 = filtro2.filtrar(*r2) if r2 else None
            if f1 and f2:
                display.atualizar_temperatura_umidade(f1[0], f1[1], f2[0], f2[1])
                print("S1: {:.1f}C {:.0f}% | S2: {:.1f}C {:.0f}%".format(f1[0], f1[1], f2[0], f2[1]))
            else:
                print("Leitura inválida")

            GPIO.setup(DHT_PIN, GPIO.OUT)
            GPIO.output(DHT_PIN, GPIO.HIGH)
            GPIO.setup(DHT_PIN2, GPIO.OUT)
            GPIO.output(DHT_PIN2, GPIO.HIGH)

            time.sleep(4)
    return threading.Thread(target=ler, daemon=True)
