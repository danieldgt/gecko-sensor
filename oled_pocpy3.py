import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import time

# Inicializa o display com I2C (sem reset pin)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

# Inicializa hardware
disp.begin()
disp.clear()
disp.display()

# Cria uma imagem preta
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Fonte padrão
font = ImageFont.load_default()

# Escreve texto na imagem
draw.text((0, 0), 'Terrario Gecko', font=font, fill=255)
draw.text((0, 20), 'Temp: 33.2 C', font=font, fill=255)
draw.text((0, 35), 'Umidade: 56%', font=font, fill=255)

# Exibe no display
disp.image(image)
disp.display()
