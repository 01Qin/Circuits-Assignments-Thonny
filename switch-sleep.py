from machine import Pin
import time

switch = Pin(7, Pin.IN, Pin.PULL_UP)  # sw 2
while True:
    if switch() == 1:
        print('switch is 1')
        time.sleep(0.5)

    else:
        print('switch is 0')
        time.sleep(0.5)