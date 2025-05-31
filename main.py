import display
import time
import le_dht22
import ASUS.GPIO as GPIO
# Inicia o display e a thread de atualização automática
display.iniciar_display()

# Atualiza dados da página 2 (informações do Gecko)
display.atualizar_gecko(nome="Maracujá", idade="6 meses")


# Inicialização
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Atualiza dados da página 1 (status dos relés)
display.atualizar_reles({
    'R1': True,   # ligado
    'R2': False,  # desligado
    'R3': True,
    'R4': False
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
