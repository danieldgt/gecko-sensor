#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>
#include <ASUS_GPIO.h>

#define MAX_TIMINGS 85
#define DHT_PIN 7  // pino físico (BOARD) 7 = GPIO 4

int data[5] = {0, 0, 0, 0, 0};

int main(void) {
    int laststate = 1;
    int counter = 0;
    int j = 0, i;

    GPIO_setwarnings(0);
    GPIO_setmode(GPIO_BOARD);
    GPIO_setup(DHT_PIN, GPIO_OUT);
    GPIO_output(DHT_PIN, 1);
    usleep(500000);  // 500ms

    GPIO_output(DHT_PIN, 0);
    usleep(20000);   // 20ms
    GPIO_output(DHT_PIN, 1);
    GPIO_setup(DHT_PIN, GPIO_IN);

    for (i = 0; i < MAX_TIMINGS; i++) {
        counter = 0;
        while (GPIO_input(DHT_PIN) == laststate) {
            counter++;
            usleep(1);
            if (counter == 255) {
                break;
            }
        }

        laststate = GPIO_input(DHT_PIN);

        if (counter == 255)
            break;

        // Ignore first 3 transitions
        if ((i >= 4) && (i % 2 == 0)) {
            data[j / 8] <<= 1;
            if (counter > 16)
                data[j / 8] |= 1;
            j++;
        }
    }

    if ((j >= 40) &&
        (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF))) {
        float h = data[0];
        float t = data[2];
        printf("HUMIDADE: %.1f\n", h);
        printf("TEMPERATURA: %.1f\n", t);
        return 0;
    } else {
        printf("FALHA: leitura inválida.\n");
        return 1;
    }
}
