import pigpio
import time
import DHT22  # Este é um arquivo dht22 personalizado que você irá criar abaixo

pi = pigpio.pi()  # Conecta ao daemon pigpiod

if not pi.connected:
    print("Erro: pigpio daemon não está rodando.")
    exit()

sensor = DHT22.sensor(pi, 4)  # GPIO 4 (ajuste conforme necessário)
sensor.trigger()

time.sleep(2)  # Espera os dados estarem disponíveis

humidity = sensor.humidity()
temperature = sensor.temperature()

if humidity is not None:
    print(f"Umidade: {humidity:.1f}%")
    print(f"Temperatura: {temperature:.1f}°C")
else:
    print("Erro na leitura.")

sensor.cancel()
pi.stop()
