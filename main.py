import display

display.iniciar_display()

display.atualizar_gecko("Ziggy", "8 meses")
display.atualizar_reles({'R1': True, 'R2': False, 'R3': True, 'R4': False})

while True:
    # aqui você atualizaria com dados reais
    display.atualizar_temperatura_umidade(32.4, 57.8, 28.1, 60)
    time.sleep(5)
