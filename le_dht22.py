import display
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

# ======== Classe de filtro ==============
class SensorFiltro:
    def __init__(self, max_len=5, tolerancia=5.0):
        self.temperaturas = []
        self.umidades = []
        self.max_len = max_len
        self.tolerancia = tolerancia

    def filtrar(self, nova_temp, nova_umid):
        if nova_temp == 0.0 or nova_umid == 0.0:
            return None  # valor suspeito

        if not self.temperaturas or not self.umidades:
            self._add(nova_temp, nova_umid)
            return nova_temp, nova_umid

        media_temp = sum(self.temperaturas) / len(self.temperaturas)
        media_umid = sum(self.umidades) / len(self.umidades)

        if (abs(nova_temp - media_temp) > self.tolerancia or
            abs(nova_umid - media_umid) > self.tolerancia):
            return None  # outlier

        self._add(nova_temp, nova_umid)
        return nova_temp, nova_umid

    def _add(self, temp, umid):
        self.temperaturas.append(temp)
        self.umidades.append(umid)
        if len(self.temperaturas) > self.max_len:
            self.temperaturas.pop(0)
            self.umidades.pop(0)

# Thread para piscar LEDs na sequência especificada
# def piscar_leds_sequencia():
#    ordem = ['Amarelo', 'Azul', 'Vermelho', 'Verde', 'Vermelho', 'Azul', 'Amarelo']
#    while True:
#        for cor in ordem:
#            for c, pin in LED_PINS.items():
#                GPIO.output(pin, GPIO.HIGH if c == cor else GPIO.LOW)
#            time.sleep(0.5)  # Pisca a cada 200ms

def monitorar_leds_parametrizado(
    limite_baixo=27.5,
    limite_ideal=31.0,
    limite_alerta=32.0,
    tempo_alerta=30
):
    fora_faixa = False
    tempo_fora = None

    while True:
        temp = display.dados_display['temp1']

        if temp == 0.0:
            time.sleep(1)
            continue

        agora = time.time()

        # Determina faixa
        dentro_faixa = limite_baixo <= temp <= limite_ideal
        acima_limite_alerta = temp > limite_alerta

        # Controla tempo fora da faixa
        if dentro_faixa:
            tempo_fora = None
            fora_faixa = False
        elif acima_limite_alerta:
            if not fora_faixa:
                tempo_fora = agora
                fora_faixa = True

        # Escolhe cor do LED
        if temp < limite_baixo:
            cor = 'Azul'
        elif temp <= limite_ideal:
            cor = 'Verde'
        else:
            cor = 'Vermelho'

        # Alerta por tempo acima do limite_alerta
        if fora_faixa and tempo_fora and (agora - tempo_fora) > tempo_alerta:
            # Piscar LED amarelo
            GPIO.output(LED_PINS['Azul'], GPIO.LOW)
            GPIO.output(LED_PINS['Verde'], GPIO.LOW)
            GPIO.output(LED_PINS['Vermelho'], GPIO.LOW)
            GPIO.output(LED_PINS['Amarelo'], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED_PINS['Amarelo'], GPIO.LOW)
            time.sleep(0.5)
            continue

        # Liga apenas o LED da faixa correspondente
        for nome, pin in LED_PINS.items():
            GPIO.output(pin, GPIO.HIGH if nome == cor else GPIO.LOW)

        time.sleep(1)

# Thread para ler sensores com filtragem
def ler_sensores():
    filtro1 = SensorFiltro()
    filtro2 = SensorFiltro()
    try:
        while True:
            result = read_dht22(DHT_PIN)
            result2 = read_dht22(DHT_PIN2)

            if result:
                temp1, hum1 = result
                f1 = filtro1.filtrar(temp1, hum1)
            else:
                f1 = None

            if result2:
                temp2, hum2 = result2
                f2 = filtro2.filtrar(temp2, hum2)
            else:
                f2 = None

            if f1 and f2:
                display.atualizar_temperatura_umidade(f1[0], f1[1], f2[0], f2[1])
                print("S1: {:.1f}°C {:.0f}% | S2: {:.1f}°C {:.0f}%".format(
                    f1[0], f1[1], f2[0], f2[1]))
            else:
                print("Leitura inválida ou fora de padrão")

            GPIO.setup(DHT_PIN, GPIO.OUT)
            GPIO.output(DHT_PIN, GPIO.HIGH)
            GPIO.setup(DHT_PIN2, GPIO.OUT)
            GPIO.output(DHT_PIN2, GPIO.HIGH)

            time.sleep(4)
    except KeyboardInterrupt:
        GPIO.cleanup()

# Inicia threads separadas
# Funções para retornar as threads (para uso em main.py)
def thread_leds():
    return threading.Thread(target=piscar_leds_sequencia, daemon=True)

def thread_sensores():
    return threading.Thread(target=ler_sensores, daemon=True)

