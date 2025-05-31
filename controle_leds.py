# controle_leds.py
import ASUS.GPIO as GPIO
import time
import threading
import display

LED_PINS = {
    'Azul': 11,
    'Verde': 13,
    'Vermelho': 15,
    'Amarelo': 16
}

PORTA_1_RELE = 18;

for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(PORTA_1_RELE, GPIO.OUT)
GPIO.output(PORTA_1_RELE, GPIO.HIGH)

def thread_leds(temp_critica=31.0, faixa_baixa=27.5, faixa_media=30.0, tempo_critico=30):
    def monitorar():
        inicio_temp_alta = None
        while True:
            t1 = display.dados_display['temp1']
    
            # Faixas de temperatura com cores
            if t1 < faixa_baixa:
                GPIO.output(LED_PINS['Azul'], GPIO.HIGH)
                GPIO.output(LED_PINS['Verde'], GPIO.LOW)
                GPIO.output(LED_PINS['Vermelho'], GPIO.LOW)
                inicio_temp_alta = None
            elif t1 < faixa_media:
                GPIO.output(LED_PINS['Azul'], GPIO.LOW)
                GPIO.output(LED_PINS['Verde'], GPIO.HIGH)
                GPIO.output(LED_PINS['Vermelho'], GPIO.LOW)
                inicio_temp_alta = None
            else:
                GPIO.output(LED_PINS['Azul'], GPIO.LOW)
                GPIO.output(LED_PINS['Verde'], GPIO.LOW)
                GPIO.output(LED_PINS['Vermelho'], GPIO.HIGH)
                # Só começa a contar o tempo se ultrapassou a faixa crítica
                if t1 >= temp_critica:
                    if inicio_temp_alta is None:
                        inicio_temp_alta = time.time()
                else:
                    inicio_temp_alta = None  # temperatura baixou antes da crítica
    
            # Pisca amarelo se passou o tempo crítico
            if inicio_temp_alta and (time.time() - inicio_temp_alta >= tempo_critico):
                GPIO.output(PORTA_1_RELE, GPIO.LOW)
                GPIO.output(LED_PINS['Amarelo'], GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LED_PINS['Amarelo'], GPIO.LOW)
                time.sleep(0.2)
            else:
                GPIO.output(PORTA_1_RELE, GPIO.HIGH)
                GPIO.output(LED_PINS['Amarelo'], GPIO.LOW)
                time.sleep(2)
    return threading.Thread(target=monitorar, daemon=True)
