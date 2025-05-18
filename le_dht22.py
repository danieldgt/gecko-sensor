import pigpio
import dht
import time

pi = pigpio.pi()
sensor = dht.sensor(pi, 4)  # GPIO4

while True:
    humidity, temperature = sensor.read()
    if humidity is not None:
        print(f"Umidade: {humidity:.1f}%")
        print(f"Temperatura: {temperature:.1f}°C")
    else:
        print("Erro na leitura")
    time.sleep(2)
