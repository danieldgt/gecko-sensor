import ASUS.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Definindo os pinos do relé
RELE_PINS = {
    'TocaAquecida': 18,
    'Umidificador': 22,
    'Cooler': 29,
    'Extra': 31
}

# Configura todos os relés como saída e em estado desligado (alto)
for pin in RELE_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # HIGH = desligado para esse módulo

# Função para ligar um relé (nível lógico baixo)
def ligar_rele(nome):
    GPIO.output(RELE_PINS[nome], GPIO.LOW)

# Função para desligar um relé (nível lógico alto)
def desligar_rele(nome):
    GPIO.output(RELE_PINS[nome], GPIO.HIGH)

# Teste simples
ligar_rele('TocaAquecida')
time.sleep(2)
desligar_rele('TocaAquecida')

GPIO.cleanup()
