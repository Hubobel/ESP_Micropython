from time import sleep
from machine import Pin, TouchPad

touch = TouchPad(Pin(12))
threshold = []

for x in range(12):
    threshold.append(touch.read())
    sleep(.1)

threshold = sum(threshold)//len(threshold)
print('Threshold: {0}'.format(threshold))

try:
    while True:
        capacitance = touch.read()
        cap_ratio = capacitance / threshold
        if .40 < cap_ratio < .95:
            print('Touch: {0}, Diff {1},Ratio: {2}%.'.format(
                capacitance, threshold-capacitance, cap_ratio*100))
            sleep(.2)
except KeyboardInterrupt:
    print('Abbruch')

