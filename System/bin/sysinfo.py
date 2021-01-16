#!/usr/bin/env python3

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

padding = -2
top = padding
bottom = height-padding
x=0

font = ImageFont.load_default()

while True:
  draw.rectangle((0,0,width,height), outline=0, fill=0)

  #cmd = "hostname -I | cut -d\' \' -f1"
  #IP = subprocess.check_output(cmd, shell=True).decode('utf-8')
  #cmd = "top -bn1 | grep load | awk '{printf $11}' | tr -d ','"
  #CPU = float(subprocess.check_output(cmd, shell=True).decode('utf-8'))
  #cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
  #RAM = subprocess.check_output(cmd, shell=True).decode('utf-8')
  #cmd = "df -h | awk '$NF==\"/\" {printf \"%s\",$5}'"
  #DISK = subprocess.check_output(cmd, shell=True).decode('utf-8')
  IP = ""
  CPU = psutil.cpu_percent()
  RAM = psutil.phymem_usage().percent
  DISK = psutil.disk_usage('/').percent

  draw.text((x,top),    "IP:   " + str(IP), font=font, fill=255)
  draw.text((x,top+8),  "CPU:  " + str(CPU) + '%', font=font, fill=255)
  draw.text((x,top+16), "RAM:  " + str(RAM), font=font, fill=255)
  draw.text((x,top+24), "DISK: " + str(DISK), font=font, fill=255)

  disp.image(image)
  disp.display()

  sleep(.1)
