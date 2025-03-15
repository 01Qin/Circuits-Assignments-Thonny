from machine import Pin
import time

#sw0 9
#sw1 8
#sw2 7
#led1 - 22
#led2 - 21
#led3 - 20


class ASM_test:
    def __init__(self, delay, led1, led2):
        self.delay = delay
        self.led1 = Pin(led1, Pin.OUT)
        self.led2 = Pin(led2, Pin.OUT)
        self.state = self.on1

    def execute(self):
        self.state()

    def on1(self):
        self.led1.on()
        self.led2.off()
        time.sleep(self.delay)
        self.state = self.on2

    def on2(self):
        self.led1.off()
        self.led2.on()
        time.sleep(self.delay)
        self.state = self.on1


asm = ASM_test(0.5, 20, 21)

while True:
    asm.execute()