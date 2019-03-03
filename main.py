import machine
import bme280
import time
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

#todo integer Wert publishen
#todo subscriben

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
            oled.pixel(127, 10, 1)
            c.disconnect()
        except:
            oled.pixel(117, 10, 1)
    else:
        station.connect("Hubobel", "PL19zPL19z")
    oled.text('Temp. '+str(t),0,0)
    oled.text('Druck '+str(p),0,10)
    oled.text('Feucht. '+str(h),0,20)
    oled.show()
    time.sleep(2)

