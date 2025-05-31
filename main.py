import display
import le_dht22
import controle_leds
import time

display.iniciar_display()
display.atualizar_gecko("Maracujá", "6 meses")
display.atualizar_reles({'R1': True, 'R2': False, 'R3': True, 'R4': False})

# Parâmetros de temperatura
zona_fria = 27.5
zona_quente = 30.0
critica = 31.0
tempo_critico = 30

thread_sensor = le_dht22.thread_sensores()
thread_led = controle_leds.thread_leds(
    temp_critica=critica,
    faixa_baixa=zona_fria,
    faixa_media=zona_quente,
    tempo_critico=tempo_critico
)

thread_sensor.start()
thread_led.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando")
