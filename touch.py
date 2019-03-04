from time import sleep
from machine import Pin, TouchPad
import machine
import bme280
import ssd1306
import network

from umqtt.simple import MQTTClient
import ubinascii

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'Test/esp'+str(CLIENT_ID)
TOPIC = TOPIC.replace("'","_")

try:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect("Hubobel", "PL19zPL19z")
except:
    None

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
touch = TouchPad(Pin(12))
threshold = []

for x in range(12):
    threshold.append(touch.read())
    sleep(.1)

threshold = sum(threshold)//len(threshold)
print('Threshold: {0}'.format(threshold))
release=True
a=1
try:
    while True:
        capacitance = touch.read()
        cap_ratio = capacitance / threshold
        if .40 < cap_ratio < .95:
            print('Touch: {0}, Diff {1},Ratio: {2}%.'.format(
                capacitance, threshold-capacitance, cap_ratio*100))
            sleep(.2)
            a = a + 1
        if a == 4:
            a=1
        if a == 1:
            print('Seite 1')
        if a == 2:
            print('Seite 2')
        if a == 3:
            print('Seite 3')

except KeyboardInterrupt:
    print('Abbruch')

