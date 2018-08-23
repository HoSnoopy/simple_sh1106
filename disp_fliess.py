#!/usr/bin/python3
#coding: utf-8

#Dieses Script zeigt Wetterdaten von einer Textdatei und System-Statusmeldungen an. Dabei wandert der Text nach oben weg und wieder nach unten. 

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.core.virtual import viewport
from PIL import ImageFont, ImageDraw, Image
from pathlib import Path
import time
import datetime
import psutil
import os

serial = i2c(port=1, address=0x3C)

device = sh1106(serial)

font = ImageFont.truetype('FreeSans.ttf', 14) # Font auswählen
bold = ImageFont.truetype('FreeSansBold.ttf', 14) # Font (Fett) auswählen

file = '/opt/autofs/daten/temp/dht_curr.dat' #Wetter-File, von einem externen Raspbery-Pi
filexists=Path(file)


virtual = viewport(device, width=device.width, height=140) #Initiieren des virtuellen Bildschirmes mit 140 Pixel Höhe und der original-breite des SD1106.

while True:
 if filexists.is_file(): 
     d = open(file, 'r')
     for zeile in d:
          z = zeile #Gehe Zeile für Zeile des Files durch
     zeit = zeile[11:16] #Extrahiere Zeit
     temp = zeile[75:79] #Extrahiere Temperatur
     lf = zeile[80:84]   #Extrahiere Luftfeuchtigkeit
     rpit = zeile[85:89] #Extrahiere Temperatur des Mess-Pis.

     w = os.popen('iwconfig wlan0 |grep Quali |cut -c 24-25') #Extrahiere die Qualität des WLAN-Empfangs des Lokalen Raspis
     wlan = str(w.read()) 
     wlan = wlan[:2]
     if wlan == '':
        wlan='Kein WLAN vorhanden.'

     i = os.popen('ifconfig wlan0 |grep 255.255.255.0 |cut -c 10-') #Extrahiere die Qualität des WLAN-Empfangs des Lokalen Raspis
     i = str(i.read())
     ip = (i.rstrip().split(' '))[1]
     
     t = os.popen('vcgencmd measure_temp |cut -c 6-9') #Extrahiere Lokale Temperatur
     t = str(t.read()) 
     t = t[:-1]

     zeit = str(time.strftime("%H:%M"))  # Extrahiere Lokalzeit

     with canvas(virtual) as draw: #Fange an zu schreiben
#Ich habe als Fontgrösse 14 festgelet. Zeilenabstand ist entsprechend 15 Pixel.
#Schribe anschliessend die oben extrahierten Werte ins virtuelle Display

          draw.text((1,1), "Wetter (" + zeit + "Uhr):", font=bold, fill=1)
          draw.text((1,16), ("Temp: " + temp + "°C"), font=font, fill=1)
          draw.text((1,31), ("LF: " + lf + "%"), font=font, fill=1)
          draw.text((1,46), ("Raspi-Temp: " + rpit + "°C"), font=font, fill=1)
          draw.text((1,61), ("Lokal ("+ zeit + "Uhr):" ), font=bold, fill=1) 
          draw.text((1,76), ("WLAN-Sig: " + wlan + "%"), font=font, fill=1)
          draw.text((1,91), ("IP: " + ip), font=font, fill=1)
          draw.text((1,106), ("Temp: " + t + "°C"), font=font, fill=1)
          
#Der Obere Bereich (Zeile 1-60) wird nun angezeigt
     time.sleep(10)  #Warte 10 Sekunden
          
     for y in range(62):  #Wechsle fliessend zum unteren Bereich
             virtual.set_position((0, y))
             
     time.sleep(10) #Warte erneut 10 Sekunden
          
   
     for y in range(62): #Wechsle fliessend zum oberen Bereich
            virtual.set_position((0, (61-y)))


 else:
     draw.text((1,1), file , font=font, fill=1)
     draw.text((12,1), "gibt's nicht!" , font=font, fill=1)
 time.sleep (5) #Warte 5 Sekunden
