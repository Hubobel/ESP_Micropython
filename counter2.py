from machine import Pin
import machine
from umqtt.simple import MQTTClient
import ubinascii


impulse = False
a = 0

def handle_interrupt(pin):
  global impulse
  impulse = True

def sub_cb(TOPIC, msg):
    global state
    print((TOPIC, msg))
    global a
    a = int(msg)
    a = a + 1

imp = Pin(15, Pin.IN)
imp.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'Test/esp'+str(CLIENT_ID)
TOPIC = TOPIC.replace("'","_")
TOPIC = TOPIC + '/Zaehler'
c = MQTTClient('client_esp', '10.0.1.59', port=1884, user='hubobel', password='polier2003')
c.set_callback(sub_cb)


while True:
    if impulse:
        print('Impulse !!!!' + str(a))
        c.connect()
        c.subscribe(TOPIC)
        c.publish(TOPIC, str(a))
        c.disconnect()
        impulse = False
