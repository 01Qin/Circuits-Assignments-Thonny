from machine import Pin
import time

led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(20, Pin.OUT)


class Button:
    def __init__(self, id):
        self.button = Pin(id, Pin.IN, pull=Pin.PULL_UP)
        self.number = 0

    def pressed(self):
        if self.button.value() == 0:
            time.sleep(0.050)

            if self.button.value() == 0:
                print('Button pressed')

                if self.number < 7:
                    self.number += 1
                else:
                    self.number = 0
                print(self.number)
                time.sleep(0.3)
        else:
            time.sleep(0.1)

            if self.number & 1:
                led1.on()
            else:
                led1.off()

            if self.number & 2:
                led2.on()
            else:
                led2.off()

            if self.number & 4:
                led3.on()
            else:
                led3.off()


button = Button(12)

while True:
    button.pressed()