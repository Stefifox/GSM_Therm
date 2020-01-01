from typing import re

import Adafruit_DHT
from gpiozero import Button, LED
from time import sleep
import time
import Lettura
import socket
import RPi.GPIO as GPIO
from Oled import welcome, base, off, err
from Adafruit_SSD1306 import SSD1306_128_64
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Oled Def

RST = 0

disp = SSD1306_128_64(rst=RST)
disp.begin()

width = disp.width
height = disp.height

padding = -2
top = padding

bottom = height - padding
x = 0
font = ImageFont.load_default()

# Code here
sver = "0.4"

screenOn = Button(23)

# Menu buttons
bMen = Button(25)
bOk = Button(1)
bUp = Button(8)  # >
bDw = Button(7)  # <

# Costanti
sec_temp = 5.0
fine = 1 * 15

active = True
men_act = False
man_temp = 20.0

relay = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)


def start():
    print("Avvio...")
    GPIO.output(relay, GPIO.LOW)
    welcome(sver)
    sleep(5)
    temper = Lettura.temp()
    umid = Lettura.umid()
    base(temper, umid, "----", active)
    rel(float(temper), 0.0)
    loop()


def loop():
    global active, men_act, man_temp
    mostra = 1
    temper = 0
    umid = 0
    hman = 0
    start_time = time.time()

    file = open("program.txt", "r")
    prog_temp = file.read().split(",")
    file.close()

    #           24  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23
    # prog_temp = 24, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23

    # print(str(time.strftime("%M:%S")) + " - " + str(temper) + " " + str(umid) + " LED: " + str(
    #    led.is_active) + " Screen: " + str(screenOn.is_pressed))

    while True:

        tAttuale = time.time() - start_time
        h = int(time.strftime("%H")) - 1

        # Verifica Temperatura e Umidità
        if tAttuale >= fine:
            start_time = time.time()
            temper = Lettura.temp()
            umid = Lettura.umid()
            print(str(time.strftime("%M:%S")) + " - " + str(temper) + " " + str(umid) + " Screen: " + str(
                screenOn.is_pressed) + " men: " + str(men_act))
            if screenOn.is_pressed and (not men_act) and active:
                base(temper, umid, prog_temp[h], active)
            if screenOn.is_pressed and (not men_act) and (not active):
                base(temper, umid, man_temp, active)
            if not screenOn.is_pressed:
                off()

            # Controllo minimo di sicurezza
            try:
                if active:
                    rel(float(temper), float(prog_temp[h]))
                else:
                    rel(float(temper), float(man_temp))
                print("ok 4")
            except:
                print("Error - Temp")
                temper = Lettura.temp()
                umid = Lettura.umid()
                err("Lettura temperatura", "----")

        # Se attivo leggo la programmazione

        if bMen.is_pressed:
            # men_act = True
            # menu()
            print("Menù non disponibile")
            err("Non disponibile", temper)

        if bOk.is_pressed:
            if mostra == 1:
                mostra = 2
            if mostra == 2:
                mostra = 1
            print("Mostro: " + str(mostra))
            err("Non disponibile", temper)

        if bUp.is_pressed:
            temper = Lettura.temp()
            umid = Lettura.umid()
            active = False
            man_temp = man_temp + 1
            hman = int(time.strftime("%H"))
            base(temper, umid, man_temp, active)
            print("Temp set: " + str(man_temp) + " H Fine: " + str(hman + 1))
        if bDw.is_pressed:
            temper = Lettura.temp()
            umid = Lettura.umid()
            active = False
            man_temp = man_temp - 1
            hman = int(time.strftime("%H"))
            base(temper, umid, man_temp, active)
            print("Temp set: " + str(man_temp) + " H Fine: " + str(hman + 1))

        if not active and hman < h:
            
            active = True
            hman = 0


def rel(temper, temp):
    relay = 21
    print("ok 0")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay, GPIO.OUT)

    print("ok 1")
    if temper < sec_temp:
        GPIO.output(relay, GPIO.HIGH)
    else:
        GPIO.output(relay, GPIO.LOW)

    print("ok 2")
    if temper < temp:
        GPIO.output(relay, GPIO.HIGH)
    else:
        GPIO.output(relay, GPIO.LOW)

    print("ok 3")


def menu():
    global active, men_act, man_temp
    temper = Lettura.temp()
    umid = Lettura.umid()

    pag = 1
    mpag = 4

    file = open("program.txt", "r")
    prog_temp = file.read().split(",")
    file.close()

    #           24  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23
    # prog_temp = 24, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23

    # print(prog_temp)

    h = int(time.strftime("%H")) - 1

    men_act = True

    pagM(1)

    sleep(0.5)
    while not bMen.is_pressed:

        if bUp.is_pressed:
            pag = pag + 1
            if pag > mpag:
                pag = 1
            pagM(pag)
        if bDw.is_pressed:
            pag = pag - 1
            if pag < 1:
                pag = 4
            pagM(pag)
        if bMen.is_pressed:
            men_act = False
        if bOk.is_pressed and pag == 4:
            off()
            exit()
        if bOk.is_pressed and pag == 3:
            if active:
                active = False
                man_temp = 5.0
            else:
                active = True
                man_temp = 20.0

    base(temper, umid, prog_temp[h], active)


def pagM(n):
    global active, men_act, man_temp
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    draw.text((x, top), "Menu", font=font, fill=255)
    draw.text((x + 64, top), "Vers: " + sver, font=font, fill=255)
    draw.text((x, top + 8), "Pag: " + str(n), font=font, fill=255)

    if n == 1:
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            draw.text((x, top + 16), "Host: " + str(host_name), font=font, fill=255)
        except:
            draw.text((x, top + 16), "Host: Error", font=font, fill=255)
        draw.text((x, top + 26), "MAC: ", font=font, fill=255)
        draw.text((x, top + 34), "Internet Mobile: ", font=font, fill=255)
    if n == 2:
        draw.text((x, top + 16), "Attivo: " + str(active), font=font, fill=255)
        draw.text((x, top + 24), "", font=font, fill=255)
        draw.text((x, top + 32), "", font=font, fill=255)
    if n == 3:
        if active:
            draw.text((x, top + 16), "Spegnere il", font=font, fill=255)
            draw.text((x, top + 24), "Termostato?", font=font, fill=255)
            draw.text((x, top + 32), "premi ok", font=font, fill=255)
        else:
            draw.text((x, top + 16), "Accendere il", font=font, fill=255)
            draw.text((x, top + 24), "Termostato?", font=font, fill=255)
            draw.text((x, top + 32), "premi ok", font=font, fill=255)
    if n == 4:
        draw.text((x, top + 16), "Spegnere il", font=font, fill=255)
        draw.text((x, top + 24), "programma?", font=font, fill=255)
        draw.text((x, top + 32), "premi ok", font=font, fill=255)

    disp.clear()
    disp.image(image)
    disp.display()
    sleep(0.5)


start()
