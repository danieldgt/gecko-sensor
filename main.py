import display
import le_dht22  # isso já inicia as threads de sensores e LEDs
import time

# Inicia o display e a thread de troca de páginas
display.iniciar_display()

# Atualiza dados da página 3 (informações do Gecko)
display.atualizar_gecko(nome="Maracujá", idade="6 meses")

# Atualiza dados da página 2 (status dos relés)
display.atualizar_reles({
    'R1': True,   # ligado
    'R2': False,  # desligado
    'R3': True,
    'R4': False
})

# Apenas mantém o programa rodando
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
