#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
from datetime import datetime
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw, ImageFont

# Inicializar pantalla
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
font = ImageFont.load_default()

def get_temp():
    temp = os.popen("vcgencmd measure_temp").read()
    return temp.replace("temp=", "").strip()

def get_freq():
    freq = os.popen("vcgencmd measure_clock arm").read()
    hz = int(freq.split("=")[-1]) // 1000000
    return f"{hz} MHz"

def get_cpu_load():
    load = os.getloadavg()[0]  # Promedio de 1 minuto
    cores = os.cpu_count()
    percent = (load / cores) * 100
    return f"{percent:.1f}%"

def draw_monitor():
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    temp = get_temp()
    freq = get_freq()
    cpu = get_cpu_load()
    now = datetime.now().strftime("%H:%M:%S %d/%m")

    draw.text((5, 5), f"Temp: {temp}", font=font, fill=1)
    draw.text((5, 20), f"Freq: {freq}", font=font, fill=1)
    draw.text((5, 35), f"CPU: {cpu}", font=font, fill=1)
    draw.text((5, 50), f"{now}", font=font, fill=1)

    device.display(image)

# Inicialización del dispositivo OLED I2C
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Cargar fuente personalizada o usar la predeterminada
try:
    font = ImageFont.truetype("DejaVuSansMono.ttf", 12)
except IOError:
    font = ImageFont.load_default()

# Función para obtener la parte simplificada de la IP LAN
def get_lan_ip_simplified():
    ip_part = '00'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.1.1.1', 1))
        ip_full = s.getsockname()[0]
        ip_parts = ip_full.split('.')
        if len(ip_parts) == 4:
            last_part = ip_parts[-1]
            ip_part = last_part[-2:] if len(last_part) >= 2 else last_part.zfill(2)
    except socket.error:
        pass
    finally:
        s.close()
    return ip_part

# Función para obtener la parte simplificada de la IP WAN
def get_wan_ip_simplified():
    wan_ip_part = '00'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_full = s.getsockname()[0]
        ip_parts = ip_full.split('.')
        if len(ip_parts) == 4:
            last_part = ip_parts[-1]
            wan_ip_part = last_part[-2:] if len(last_part) >= 2 else last_part.zfill(2)
    except socket.error:
        pass
    finally:
        s.close()
    return wan_ip_part

# Logo de Batman en pixel art

zoom_factor = 2
logo_width = 27 * zoom_factor  # → 54
logo_height = 11 * zoom_factor # → 22

logo_x = (128 - logo_width) // 2  # → 37
logo_y = 64 - 22 - 1


width = 27
height = 11
batlogo2 = [
    0x01, 0x03, 0x07, 0x3f, 0x3f, 0x3f, 0x7f, 0x7f, 0x7e, 0xfc, 0xf8, 0xf8, 0xfe, 0xfc, 0xfe, 0xf8,
    0xf8, 0xfc, 0x7e, 0x7f, 0x7f, 0x3f, 0x3f, 0x3f, 0x07, 0x03, 0x01
]

def draw_batman_logo(draw, x_offset, y_offset, scale=2):
    for y in range(height):
        for x in range(width):
            byte_index = x
            bit_index = y
            if byte_index < len(batlogo2):
                byte = batlogo2[byte_index]
                pixel_on = (byte >> bit_index) & 0x01
                if pixel_on:
                    draw.rectangle(
                        (
                            x_offset + x * scale,
                            y_offset + y * scale,
                            x_offset + x * scale + scale - 1,
                            y_offset + y * scale + scale - 1
                        ),
                        fill="white"
                    )

# Bucle principal
try:
    while True:
        try:
            lan_ip = get_lan_ip_simplified()
            wan_ip = get_wan_ip_simplified()

            with canvas(device) as draw:
                draw.text((0, 0), f"LAN:{lan_ip} WAN:{wan_ip}", font=font, fill="white")
                now = datetime.now()
                draw.text((0, 15), now.strftime("%H:%M  %d-%m-%Y"), font=font, fill="white")
                draw_batman_logo(draw, logo_x, logo_y, scale=2)

        except Exception as e:
            with canvas(device) as draw:
                draw.text((0, 0), "Error:", font=font, fill="white")
                draw.text((0, 15), str(e), font=font, fill="white")

        time.sleep(5)

except KeyboardInterrupt:
    print("Interrupción por teclado. Cerrando pantalla...")
    device.clear()
