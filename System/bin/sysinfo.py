#!/usr/bin/env python3
"""
This script displays some system information on an I2C connected OLED display
"""

import threading
from time import sleep
import psutil
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_address=0x3c)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.load_default()

def get_net_info(if_name):
  return [ip.address for ip in psutil.net_if_addrs()[if_name] if ip.family.value==2]

def main_thread():
  while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    WLAN = get_net_info('wlan0')[0]
    CPU = psutil.cpu_percent()
    RAM = psutil.virtual_memory().percent
    DISK = psutil.disk_usage('/').percent

    draw.text((0,-2), "IP:  " + str(WLAN), font=font, fill=255)
    draw.text((0,6), "CPU:  " + str(CPU), font=font, fill=255)
    draw.text((0,14), "RAM:  " + str(RAM), font=font, fill=255)
    draw.text((0,22), "DISK: " + str(DISK), font=font, fill=255)

    disp.image(image)
    disp.display()
    sleep(.25)

sysinfo_thread = threading.Thread(target=main_thread, daemon=True)

if __name__ == '__main__':
  """
  This simple test:
   - starts the main_thread
   - lets it run for 10 seconds
   - forcefully kills the thread when the script exits
  """
  sysinfo_thread.start()
  sleep(10)
 
