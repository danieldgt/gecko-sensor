import display
import le_dht22
import time

# Inicia o display e a thread de alternância de páginas
display.iniciar_display()

# Atualiza informações fixas
display.atualizar_gecko(nome="Maracujá", idade="6 meses")
display.atualizar_reles({
    'R1': True,
    'R2': False,
    'R3': True,
    'R4': False
})

# Inicia as threads de sensores e LEDs
thread_leds = threading.Thread(
    target=lambda: le_dht22.monitorar_leds_parametrizado(
        limite_baixo=27.5,
        limite_ideal=31.0,
        limite_alerta=32.0,
        tempo_alerta=30
    ),
    daemon=True
)
thread_leds.start()

thread_sensores = le_dht22.thread_sensores()
thread_sensores.start()

# Mantém o programa principal vivo
while True:
    time.sleep(1)
