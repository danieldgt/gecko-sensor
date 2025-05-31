import smbus
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps
import threading
import time

I2C_ADDR = 0x3C
WIDTH = 128
HEIGHT = 64
bus = smbus.SMBus(1)

# Dados para exibição
dados_display = {
    'temp1': 0.0,
    'umid1': 0.0,
    'temp2': 0.0,
    'umid2': 0.0,
    'reles': {'R1': False, 'R2': False, 'R3': False, 'R4': False},
    'gecko': {'nome': 'Leo', 'idade': '1 ano'}
}

pagina_atual = 0
font = ImageFont.load_default()

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

def render_image():
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    global pagina_atual
    if pagina_atual == 0:
        draw.text((0, 0), "Sensor 1", font=font, fill=255)
        draw.text((0, 16), "T: {:.1f}C".format(dados_display['temp1']), font=font, fill=255)
        draw.text((0, 32), "U: {:.0f}%".format(dados_display['umid1']), font=font, fill=255)
        draw.text((0, 48), "Sensor 2 T: {:.1f}".format(dados_display['temp2']), font=font, fill=255)
    elif pagina_atual == 1:
        draw.text((0, 0), "Status Rele:", font=font, fill=255)
        y = 16
        for chave, val in dados_display['reles'].items():
            draw.text((0, y), "{}: {}".format(chave, 'ON' if val else 'OFF'), font=font, fill=255)
            y += 12
    elif pagina_atual == 2:
        draw.text((0, 0), "Gecko Leopard", font=font, fill=255)
        draw.text((0, 16), "Nome: {}".format(dados_display['gecko']['nome']), font=font, fill=255)
        draw.text((0, 32), "Idade: {}".format(dados_display['gecko']['idade']), font=font, fill=255)
    elif pagina_atual == 3:
        try:
            logo = Image.open("gecko.bmp").convert("1")
            logo = ImageOps.invert(logo)  # se necessário inverter cores
            logo = logo.resize((100, HEIGHT))
            image.paste(logo, (0, 0))
        except:
            draw.text((0, 24), "Imagem gecko.bmp", font=font, fill=255)
            draw.text((0, 40), "nao encontrada", font=font, fill=255)

    return image

def enviar_imagem(image):
    pixels = image.load()
    for page in range(0, HEIGHT // 8):
        command(0xB0 + page)
        command(0x00)
        command(0x10)
        for x in range(WIDTH):
            byte = 0
            for bit in range(8):
                if pixels[x, page * 8 + bit]:
                    byte |= (1 << bit)
            data(byte)

def loop_display():
    global pagina_atual
    while True:
        img = render_image()
        enviar_imagem(img)
        time.sleep(4)
        pagina_atual = (pagina_atual + 1) % 4

# Interfaces públicas:

def iniciar_display():
    init_display()
    t = threading.Thread(target=loop_display, daemon=True)
    t.start()

def atualizar_temperatura_umidade(t1, u1, t2, u2):
    dados_display['temp1'] = t1
    dados_display['umid1'] = u1
    dados_display['temp2'] = t2
    dados_display['umid2'] = u2

def atualizar_reles(rele_dict):
    dados_display['reles'] = rele_dict

def atualizar_gecko(nome, idade):
    dados_display['gecko']['nome'] = nome
    dados_display['gecko']['idade'] = idade
