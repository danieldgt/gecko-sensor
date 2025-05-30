from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

import time

# Inicializa o display
serial = i2c(port=1, address=0x3C)  # Endereço I2C padrão do SSD1306
device = ssd1306(serial, width=128, height=64)

# Exibe uma mensagem de teste
with canvas(device) as draw:
    draw.text((0, 0), "Terrario Gecko", fill=255)
    draw.text((0, 16), "Temp: 33.1C", fill=255)
    draw.text((0, 32), "Umid: 58%", fill=255)
    draw.text((0, 48), "Toca: Ligada", fill=255)

time.sleep(5)
device.clear()
