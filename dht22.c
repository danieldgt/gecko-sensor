#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_TIMINGS 85
#define GPIO 164  // Pino físico 11 na Tinker Board S

int read_gpio() {
    char path[50], value_str[3];
    sprintf(path, "/sys/class/gpio/gpio%d/value", GPIO);
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    read(fd, value_str, 3);
    close(fd);
    return atoi(value_str);
}

void write_gpio(int value) {
    char path[50];
    sprintf(path, "/sys/class/gpio/gpio%d/value", GPIO);
    int fd = open(path, O_WRONLY);
    if (fd < 0) return;
    write(fd, value ? "1" : "0", 1);
    close(fd);
}

void set_direction(const char* dir) {
    char path[50];
    sprintf(path, "/sys/class/gpio/gpio%d/direction", GPIO);
    int fd = open(path, O_WRONLY);
    if (fd < 0) return;
    write(fd, dir, strlen(dir));
    close(fd);
}

void export_gpio() {
    FILE *f = fopen("/sys/class/gpio/export", "w");
    if (f) {
        fprintf(f, "%d", GPIO);
        fclose(f);
        usleep(100000);
    }
}

void read_dht22() {
    int data[5] = {0, 0, 0, 0, 0};
    int last_state = 1, counter = 0, i;
    int timings[MAX_TIMINGS];

    export_gpio();
    set_direction("out");

    // Start signal: LOW por pelo menos 1ms (18ms padrão)
    write_gpio(0);
    usleep(18000);  // 18 ms
    write_gpio(1);
    usleep(40);     // 40 us

    set_direction("in");

    // Coleta pulsos (LOW + HIGH)
    for (i = 0; i < MAX_TIMINGS; i++) {
        counter = 0;
        while (read_gpio() == last_state) {
            counter++;
            usleep(1);
            if (counter >= 255) break;
        }
        last_state = read_gpio();
        timings[i] = counter;
    }

    // Processa os bits
    int bit_index = 0;
    for (i = 0; i < MAX_TIMINGS - 1 && bit_index < 40; i++) {
        int low = timings[i];
        int high = timings[i + 1];

        // Ignora os primeiros pares (resposta do sensor)
        if (i < 4) continue;

        data[bit_index / 8] <<= 1;
        if (high > 50) {
            data[bit_index / 8] |= 1;
        }

        bit_index++;
        i++;  // avança para o próximo par
    }

    // Verifica checksum
    if (((data[0] + data[1] + data[2] + data[3]) & 0xFF) != data[4]) {
        printf("Checksum inválido: %d %d %d %d %d\n",
               data[0], data[1], data[2], data[3], data[4]);
        return;
    }

    float humidity = ((data[0] << 8) + data[1]) / 10.0;
    float temperature = ((data[2] & 0x7F) << 8 | data[3]) / 10.0;
    if (data[2] & 0x80) temperature = -temperature;

    printf("Temperatura: %.1f°C | Umidade: %.1f%%\n", temperature, humidity);
}

int main() {
    while (1) {
        read_dht22();
        sleep(2);  // Tempo mínimo entre leituras conforme datasheet
    }
    return 0;
}
