from time import sleep
from machine import Pin, TouchPad, ADC
import machine
import bme280
#import tsl2561
import ssd1306
import network

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)
pindigital=machine.Pin(15)

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
a=4
try:
    while True:
        t, p, h = bme.values
        mq_t = t.replace("C", "")
        mq_p = p.replace("hPa", "")
        mq_h = h.replace("%", "")
        oled.fill(0)
        if station.isconnected():
            oled.pixel(127, 0, 1)
            try:
                c = MQTTClient('client_esp', '10.0.1.59', port=1884, user='hubobel', password='polier2003')
                c.connect()
                c.publish(TOPIC + '/Temperatur', mq_t)
                c.publish(TOPIC + '/Luftfeuchte', mq_h)
                c.publish(TOPIC + '/Luftdruck', mq_p)
                c.publish(TOPIC + '/Bodenfeuchte', str(pot_value))
                oled.pixel(127, 10, 1)
                c.disconnect()
            except:
                oled.pixel(117, 10, 1)
        else:
            station.connect("Hubobel", "PL19zPL19z")

        capacitance = touch.read()
        cap_ratio = capacitance / threshold
        digitalinput

        # if .40 < cap_ratio < .95:
        #     a += 1
        # if a == 5:
        #     a = 1
        if a == 1:
            oled.text('Temperatur',0,0)
            oled.text(str(t), 0, 10)
            oled.show()
        if a == 2:
            oled.text('Luftdruck',0,0)
            oled.text(str(p), 0, 10)
            oled.show()
        if a == 3:
            oled.text('Luftfeuchte',0,0)
            oled.text(str(h), 0, 10)
            oled.show()
        if a == 4:
            pot_value = pot.read()
            oled.text('Temp. ' + str(t), 0, 0)
            oled.text('Druck ' + str(p), 0, 10)
            #oled.text('Feucht. ' + str(h), 0, 20)
            oled.text('cap ' + str(pot_value), 0, 20)
            oled.show()
        sleep(2)
except KeyboardInterrupt:
    print('Abbruch')

