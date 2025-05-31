import smbus
import time
from PIL import Image, ImageDraw, ImageFont

I2C_ADDR = 0x3C  # Endereço padrão do SSD1306
bus = smbus.SMBus(1)  # I2C-1

# Comandos de inicialização do SSD1306
init_cmds = [
    0xAE, 0xD5, 0x80, 0xA8, 0x3F,
    0xD3, 0x00, 0x40, 0x8D, 0x14,
    0x20, 0x00, 0xA1, 0xC8, 0xDA,
    0x12, 0x81, 0xCF, 0xD9, 0xF1,
    0xDB, 0x40, 0xA4, 0xA6, 0xAF
]

def command(cmd):
    bus.write_byte_data(I2C_ADDR, 0x00, cmd)

def data(cmd):
    bus.write_byte_data(I2C_ADDR, 0x40, cmd)

# Inicializa o display
for cmd in init_cmds:
    command(cmd)

# Cria uma imagem com PIL
width = 128
height = 64
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Escreve informações na imagem
draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((0, 0),    "Terrario Gecko", font=font, fill=255)
draw.text((0, 20),   "Temp: 32.5 C", font=font, fill=255)
draw.text((0, 40),   "Umidade: 61%", font=font, fill=255)

# Envia para o display
buf = list(image.tobytes())

# Divide em pacotes de 16 bytes
for i in range(0, len(buf), 16):
    chunk = buf[i:i+16]
    for b in chunk:
        data(b)
