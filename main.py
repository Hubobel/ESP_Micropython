from time import sleep
import ssd1306
import machine
import network

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

try:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect("Hubobel", "PL19zPL19z")
    oled.text('connected', 0, 0)
    oled.show()
except:
    oled.text('not connected', 0, 0)
    oled.show()
    None

#oled.fill(0)
#oled.text('4 Sec - ctrl-C',0,0)
oled.text('4 ',0,10)
oled.show()
sleep(1)
oled.text('3 ',20,10)
oled.show()
sleep(1)
oled.text('2 ',40,10)
oled.show()
sleep(1)
oled.text('1 ',60,10)
oled.show()
sleep(1)
oled.text('Start ',0,20)
oled.show()

import touch

