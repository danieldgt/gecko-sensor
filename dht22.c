void read_dht22() {
    uint8_t laststate = HIGH;
    uint8_t counter = 0;
    uint8_t j = 0, i;

    data[0] = data[1] = data[2] = data[3] = data[4] = 0;

    pinMode(DHT_PIN, OUTPUT);
    digitalWrite(DHT_PIN, LOW);
    delay(20);  // pelo menos 1ms (20ms para garantir)
    digitalWrite(DHT_PIN, HIGH);
    delayMicroseconds(40);
    pinMode(DHT_PIN, INPUT);

    for (i = 0; i < MAX_TIMINGS; i++) {
        counter = 0;
        while (digitalRead(DHT_PIN) == laststate) {
            counter++;
            delayMicroseconds(1);
            if (counter == 255)
                break;
        }

        laststate = digitalRead(DHT_PIN);

        if (counter == 255) break;

        // ignorar os primeiros 3 pulsos
        if ((i >= 4) && (i % 2 == 0)) {
            data[j / 8] <<= 1;
            if (counter > 50)
                data[j / 8] |= 1;
            j++;
        }
    }

    // Impressão dos dados brutos recebidos
    printf("Dados recebidos: %d %d %d %d %d\n", 
        data[0], data[1], data[2], data[3], data[4]);

    if ((j >= 40) && 
        (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF))) {
        float h = (data[0] << 8 | data[1]) * 0.1;
        float t = ((data[2] & 0x7F) << 8 | data[3]) * 0.1;
        if (data[2] & 0x80) t = -t;

        printf("Umidade: %.1f %%\n", h);
        printf("Temperatura: %.1f *C\n", t);
    } else {
        printf("Falha na leitura (checksum inválido)\n");
    }
}
