import display
import le_dht22
import time

# Inicia o display e as páginas automáticas
display.iniciar_display()

# Atualiza dados fixos
display.atualizar_gecko(nome="Maracujá", idade="6 meses")
display.atualizar_reles({
    'R1': True,
    'R2': False,
    'R3': True,
    'R4': False
})

# Define os parâmetros de temperatura para os LEDs
# zona_fria < zona_normal < zona_quente < critica
zona_fria = 27.5
zona_quente = 31.0
critica = 32.0
tempo_critico = 30  # segundos

# Inicializa as threads passando os parâmetros definidos
thread_sensor = le_dht22.thread_sensores()
thread_led = le_dht22.thread_leds_temperatura(
    zona_fria=zona_fria,
    zona_quente=zona_quente,
    zona_critica=critica,
    tempo_critico=tempo_critico
)

# Inicia as threads
thread_sensor.start()
thread_led.start()
import display
import le_dht22
import time

# Inicia o display e as páginas automáticas
display.iniciar_display()

# Atualiza dados fixos
display.atualizar_gecko(nome="Maracujá", idade="6 meses")
display.atualizar_reles({
    'R1': True,
    'R2': False,
    'R3': True,
    'R4': False
})

# Define os parâmetros de temperatura para os LEDs
# zona_fria < zona_normal < zona_quente < critica
zona_fria = 27.5
zona_quente = 31.0
critica = 32.0
tempo_critico = 30  # segundos

# Inicializa as threads passando os parâmetros definidos
thread_sensor = le_dht22.thread_sensores()
thread_led = le_dht22.thread_leds_temperatura(
    zona_fria=zona_fria,
    zona_quente=zona_quente,
    zona_critica=critica,
    tempo_critico=tempo_critico
)

# Inicia as threads
thread_sensor.start()
thread_led.start()

# Mantém o programa principal vivo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando o programa.")

# Mantém o programa principal vivo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando o programa.")
