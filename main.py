import display
import time
# Inicia o display e a thread de atualização automática
display.iniciar_display()

# Atualiza dados da página 2 (informações do Gecko)
display.atualizar_gecko(nome="Maracujá", idade="6 meses")

# Atualiza dados da página 1 (status dos relés)
display.atualizar_reles({
    'Toca Aquecida': True,   # ligado
    'Toca Umida': False,  # desligado
    'Cooler': True,
    'Luz': False
})

# Loop que simula leitura de sensores a cada 5 segundos
while True:
    # Atualiza dados da página 0 (sensores)
    display.atualizar_temperatura_umidade(
        t1=32.4,
        u1=60.2,
        t2=28.9,
        u2=64.1
    )

    # Espera até a próxima leitura
    time.sleep(5)
