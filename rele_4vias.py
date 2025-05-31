import ASUS.GPIO as GPIO
import time

# Usando BOARD para usar os números físicos
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pinos conectados aos canais IN1 a IN4 do módulo relé
RELE_PINS = {
    'Rele1': 18,  # físico 18
    'Rele2': 22,  # físico 22
    'Rele3': 29,  # físico 29
    'Rele4': 31   # físico 31
}

# Configura os pinos como saída e desliga todos inicialmente
for pin in RELE_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # HIGH = desligado para relé ativo em LOW

# Teste: liga cada relé por 2 segundos
try:
    for nome, pin in RELE_PINS.items():
        print("Ligando", nome)
        GPIO.output(pin, GPIO.LOW)  # Liga
        time.sleep(2)
        GPIO.output(pin, GPIO.HIGH)  # Desliga
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
