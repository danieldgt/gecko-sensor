import ASUS.GPIO as GPIO
import time

DHT_PIN = 7  # Pino físico 7 (GPIO 4)

def read_dht22(pin):
    data = []

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    
    # Iniciar o sinal de início
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20ms
    GPIO.output(pin, GPIO.HIGH)
    GPIO.setup(pin, GPIO.IN)

    # Ler a resposta do sensor
    count = 0
    while GPIO.input(pin) == GPIO.HIGH:
        count += 1
        if count > 10000:
            print("Timeout esperando resposta do sensor (pull down)")
            return None

    # Espera pelo início dos dados
    while GPIO.input(pin) == GPIO.LOW:
        continue
    while GPIO.input(pin) == GPIO.HIGH:
        continue

    # Lê 40 bits de dados
    for i in range(40):
        while GPIO.input(pin) == GPIO.LOW:
            continue

        t = time.time()
        while GPIO.input(pin) == GPIO.HIGH:
            continue
        if time.time() - t > 0.00005:  # 50 microssegundos
            data.append(1)
        else:
            data.append(0)

    # Agrupa os bits em bytes
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = int("".join([str(i) for i in humidity_bit]), 2)
    temperature = int("".join([str(i) for i in temperature_bit]), 2)
    check = int("".join([str(i) for i in check_bit]), 2)

    if ((humidity + temperature) & 0xFF) != check:
        print("Checksum inválido")
        return None

    return humidity, temperature

# Teste
try:
    while True:
        result = read_dht22(DHT_PIN)
        if result:
            humidity, temperature = result
            print(f"Temperatura: {temperature}°C, Umidade: {humidity}%")
        else:
            print("Falha na leitura.")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
