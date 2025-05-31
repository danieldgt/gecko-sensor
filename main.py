import display
import le_dht22
import time

# Inicia o display e dados fixos
display.iniciar_display()
display.atualizar_gecko(nome="Maracujá", idade="6 meses")
display.atualizar_reles({
    'R1': True,
    'R2': False,
    'R3': True,
    'R4': False
})

# Inicia as threads
thread_leds = le_dht22.thread_leds()
thread_sensores = le_dht22.thread_sensores()

thread_leds.start()
thread_sensores.start()

# Mantém vivo o main
while True:
    time.sleep(1)
