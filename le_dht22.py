import time
import board
import adafruit_dht

# Define o pino conectado (ajuste se necessário, ex: board.D18 se for no GPIO 18)
dht_device = adafruit_dht.DHT22(board.D4)  # Ex: GPIO 4

try:
    while True:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            print(f"Temp: {temperature:.1f}°C  Umidade: {humidity:.1f}%")
        else:
            print("Falha na leitura do sensor.")

        time.sleep(2.0)

except KeyboardInterrupt:
    print("Encerrando...")

except Exception as e:
    print(f"Erro: {e}")
