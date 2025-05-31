import smbus
from PIL import Image, ImageDraw, ImageFont

I2C_ADDR = 0x3C
bus = smbus.SMBus(1)
WIDTH = 128
HEIGHT = 64

def command(cmd):
    bus.write_byte_data(I2C_ADDR, 0x00, cmd)

def data(val):
    bus.write_byte_data(I2C_ADDR, 0x40, val)

def init_display():
    cmds = [
        0xAE, 0xD5, 0x80, 0xA8, 0x3F,
        0xD3, 0x00, 0x40, 0x8D, 0x14,
        0x20, 0x00, 0xA1, 0xC8, 0xDA,
        0x12, 0x81, 0xCF, 0xD9, 0xF1,
        0xDB, 0x40, 0xA4, 0xA6, 0xAF
    ]
    for cmd in cmds:
        command(cmd)

def mostrar_status(temp1, umid1, temp2, umid2):
    # Cria uma imagem e desenha o conteúdo
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((0, 0), "Terrario Gecko", font=font, fill=255)
    draw.text((0, 16), f"T1: {temp1:.1f}C  U1: {umid1:.0f}%", font=font, fill=255)
    draw.text((0, 32), f"T2: {temp2:.1f}C  U2: {umid2:.0f}%", font=font, fill=255)

    # Converte para bytes paginados
    pixels = image.load()
    for page in range(0, HEIGHT // 8):
        command(0xB0 + page)   # page address
        command(0x00)          # lower column
        command(0x10)          # upper column
        for x in range(WIDTH):
            byte = 0
            for bit in range(8):
                if pixels[x, page * 8 + bit]:
                    byte |= (1 << bit)
            data(byte)

# Uso de exemplo:
if __name__ == "__main__":
    init_display()
    mostrar_status(33.5, 58, 29.1, 64)
