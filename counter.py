import machine
from umqtt.simple import MQTTClient
import ubinascii
import network

try:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect("Hubobel", "PL19zPL19z")
except:
    None

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'Test/esp'+str(CLIENT_ID)
TOPIC = TOPIC.replace("'","_")
c = MQTTClient('client_esp', '10.0.1.59', port=1884, user='hubobel', password='polier2003')
c.connect()

def sub_cb(TOPIC, msg):
    print((TOPIC, msg))

c.subscribe(TOPIC + '/Temperatur')

pin =machine.Pin(15)
flag = 0

while True:
    if pin.value() == 0 and flag == 0:
        print('Kontakt')
        flag = 1
    if pin.value() == 1 and flag == 1:
        print('kein Kontakt')
        flag = 0