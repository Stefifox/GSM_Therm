from gpiozero import Button
from Adafruit_SSD1306 import SSD1306_128_64
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import Adafruit_GPIO.SPI as SPIsudos

from gpiozero import CPUTemperature

cpu = CPUTemperature()

RST = 0

disp = SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

padding = -2
top = padding

bottom = height-padding
x = 0
font = ImageFont.load_default()
fontBig = ImageFont.truetype("OpenSans-Light.ttf", 30)


def base(t, u, s, act):
    tipo = 1
    disp.clear()
    disp.display()
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    sleep(0.1)

    draw.text((x, top), "Base", font=font, fill=255)
    draw.text((x + 64, top), str(time.strftime("%H:%M")) , font=font, fill=255)
    draw.text((x + 64, top + 8), "\tON: " + str(act), font=font, fill=255)

    draw.text((x, top + 16), "Temp: " + str(t), font=font, fill=255)
    draw.text((x, top + 24), "Umid: " + str(u), font=font, fill=255)
    draw.text((x, top + 32), "Set: " + str(s), font=font, fill=255)
    draw.text((x, top + 50), "CPU: " + str(cpu.temperature) + " °C", font=font, fill=255)

    if tipo == 1:
        draw.text((x + 64, top + 16), str(t), font=fontBig, fill=255)
    if tipo == 2:
        draw.text((x + 64, top + 16), str(s), font=fontBig, fill=255)

    sleep(0.1)
    disp.image(image)
    disp.display()


def err(text, temp):
    disp.clear()
    disp.display()
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    sleep(0.1)

    draw.text((x, top), "Notifica", font=font, fill=255)
    draw.text((x + 64, top), str(time.strftime("%H:%M")), font=font, fill=255)
    draw.text((x, top + 8), "CPU Temp: " + str(cpu.temperature) + " °C", font=font, fill=255)

    draw.text((x, top + 16), "Errore: ", font=font, fill=255)
    draw.text((x, top + 24), str(text), font=font, fill=255)
    draw.text((x, top + 32), "Temp: " + str(temp), font=font, fill=255)


    sleep(0.1)
    disp.image(image)
    disp.display()


def notifica(text):
    disp.clear()
    disp.display()
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    sleep(0.1)

    draw.text((x, top), "Notifica", font=font, fill=255)
    draw.text((x + 64, top), str(time.strftime("%H:%M")), font=font, fill=255)
    draw.text((x, top + 8), "CPU Temp: " + str(cpu.temperature) + " °C", font=font, fill=255)

    draw.text((x, top + 24), str(text), font=font, fill=255)

    sleep(0.1)
    disp.image(image)
    disp.display()


def welcome(vers):
    disp.clear()
    disp.display()

    image = Image.open('./pi_logo.png').convert('1')
    draw = ImageDraw.Draw(image)
    draw.text((x, top), "powered by Raspbian", font=font, fill=255)

    disp.image(image)
    disp.display()
    sleep(5)
    disp.clear()
    disp.display()
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    sleep(0.1)
    draw.text((x, top), "Avvio in corso", font=font, fill=255)
    draw.text((x, top + 16), "Benvenuto", font=font, fill=255)
    draw.text((x, top + 24), "Software version:", font=font, fill=255)
    draw.text((x, top + 32), str(vers), font=font, fill=255)
    sleep(0.1)
    disp.image(image)
    disp.display()


def off():
    disp.clear()
    disp.display()


