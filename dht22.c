#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_TIMINGS 85
#define GPIO 166  // GPIO163 = pino físico 13 (modo BOARD) no Tinker Board

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
        usleep(100000);  // aguarda o sistema criar os arquivos
    }
}

void read_dht22() {
    int data[5] = {0, 0, 0, 0, 0};
    int last_state = 1, counter = 0, i;
    int timings[MAX_TIMINGS];

    export_gpio();
    set_direction("out");

    // Sinal de início: 18ms LOW
    write_gpio(0);
    usleep(18000);
    write_gpio(1);
    usleep(40);
    set_direction("in");

    // Coleta pulsos de transição (LOW-HIGH)
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

    // Interpreta bits com base no tempo do pulso HIGH
    int bit_index = 0;
    int bit_started = 0;
    for (i = 0; i < MAX_TIMINGS; i++) {
        int duration = timings[i];

        // Aguarda os pulsos de resposta do sensor (80us LOW + 80us HIGH)
        if (!bit_started) {
            if (duration > 10 && duration < 80) {
                bit_started = 1;
            }
            continue;
        }

        // A partir daqui interpretamos os bits
        if (bit_index < 40) {
            data[bit_index / 8] <<= 1;
            if (duration > 50) {
                data[bit_index / 8] |= 1;
            }
            bit_index++;
        }
    }

    // Verifica checksum
    if (((data[0] + data[1] + data[2] + data[3]) & 0xFF) != data[4]) {
        printf("Checksum inválido: %d %d %d %d %d\n",
               data[0], data[1], data[2], data[3], data[4]);
        return;
    }

    // Conversão e exibição dos dados
    float humidity = ((data[0] << 8) + data[1]) / 10.0;
    float temperature = ((data[2] & 0x7F) << 8 | data[3]) / 10.0;
    if (data[2] & 0x80) temperature = -temperature;

      printf("Bytes lidos: %02X %02X %02X %02X %02X\n",
           data[0], data[1], data[2], data[3], data[4]);
    printf("Temperatura: %.1f°C | Umidade: %.1f%%\n", temperature, humidity);
}

int main() {
    while (1) {
        read_dht22();
        sleep(2);  // intervalo mínimo recomendado entre leituras
    }
    return 0;
}
