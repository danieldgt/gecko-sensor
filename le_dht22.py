import ASUS.GPIO as GPIO
import time

DHT_PIN = 11  # Pino físico 11 (modo BOARD)

def read_dht22(pin):
    data = []

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)  # 20 ms
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.00002)  # 20 us
    GPIO.setup(pin, GPIO.IN)

    for i in range(3000):
        data.append(GPIO.input(pin))

    bits = []
    pulse_lengths = []
    count = 0

    # Remove sinal inicial do sensor
    while count < len(data) and data[count] == 1:
        count += 1
    while count < len(data) and data[count] == 0:
        count += 1
    while count < len(data) and data[count] == 1:
        count += 1

    # Lê 40 bits de dados
    for i in range(40):
        while count < len(data) and data[count] == 0:
            count += 1
        start = count
        while count < len(data) and data[count] == 1:
            count += 1
        pulse_length = count - start
        pulse_lengths.append(pulse_length)

    # Calibra o valor de corte com base na média dos pulsos
    if len(pulse_lengths) != 40:
        print("Falha na leitura (dados incompletos)")
        return

    pulse_threshold = sum(pulse_lengths) / len(pulse_lengths)

    for pl in pulse_lengths:
        if pl > pulse_threshold:
            bits.append(1)
        else:
            bits.append(0)

    # Converte bits em bytes
    if len(bits) != 40:
        print("Falha na leitura (bits incompletos)")
        return

    bytes_ = []
    for i in range(0, 40, 8):
        byte = 0
        for j in range(8):
            byte <<= 1
            byte |= bits[i + j]
        bytes_.append(byte)

    checksum = sum(bytes_[:4]) & 0xFF
    if checksum != bytes_[4]:
        print("Checksum inválido")
        return

    humidity = ((bytes_[0] << 8) + bytes_[1]) / 10.0
    temperature = ((bytes_[2] & 0x7F) << 8 | bytes_[3]) / 10.0
    if bytes_[2] & 0x80:
        temperature = -temperature

    print("Temperatura: {:.1f}°C | Umidade: {:.1f}%".format(temperature, humidity))

# Execução
if __name__ == "__main__":
    try:
        while True:
            read_dht22(DHT_PIN)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Encerrando...")
        GPIO.cleanup()
