#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

#define MAX_TIMINGS 85
#define GPIO 164

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
    if (value)
        write(fd, "1", 1);
    else
        write(fd, "0", 1);
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
    int data[5] = {0,0,0,0,0};
    int last_state = 1, counter = 0, j = 0, i;
    int bits[MAX_TIMINGS];

    export_gpio();
    set_direction("out");
    write_gpio(0);
    usleep(18000);
    write_gpio(1);
    usleep(40);
    set_direction("in");

    for (i = 0; i < MAX_TIMINGS; i++) {
        counter = 0;
        while (read_gpio() == last_state) {
            counter++;
            usleep(1);
            if (counter == 255) break;
        }
        last_state = read_gpio();
        bits[i] = counter;
    }

    // Parse bits
    for (i = 0; i < 40; i++) {
        int idx = 3 + i * 2;
        data[i / 8] <<= 1;
        if (bits[idx] > 16)  // limiar ajustável
            data[i / 8] |= 1;
    }

    // Checksum
    if ((data[0] + data[1] + data[2] + data[3]) & 0xFF != data[4]) {
        printf("Checksum inválido\n");
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
        sleep(2);
    }
    return 0;
}
