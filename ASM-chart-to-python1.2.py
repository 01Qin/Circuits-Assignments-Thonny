from machine import Pin
import time

class AlarmControl:
    def __init__(self, alarm_pin=9, button_pin=7, red_light_pin=22, siren_pin=20):
        self.alarm = Pin(alarm_pin, Pin.IN, Pin.PULL_UP)
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.red_light = Pin(red_light_pin, Pin.OUT)
        self.siren = Pin(siren_pin, Pin.OUT)
        self.state = "idle"

    def update(self):
        if self.state == "idle":
            if self.alarm.value() == 0:  # Alarm triggered
                self.state = "alarm"
                self.red_light.on()
                self.siren.on()
        elif self.state == "alarm":
            if self.button.value() == 0:  # Button pressed
                self.state = "acknowledged"
                self.siren.off()
            elif self.alarm.value() == 1:  # Alarm deactivated
                self.state = "deactivated"
                self.red_light.on()
                self.siren.off()
        elif self.state == "acknowledged":
            if self.alarm.value() == 1:
                self.state = "idle"
                self.red_light.off()
            else:
                self.red_light.toggle()
                time.sleep_ms(500)
        elif self.state == "deactivated":
            if self.button.value() == 0:
                self.state = "idle"
                self.red_light.off()

    def run(self):
        while True:
            self.update()


alarm_control = AlarmControl()
alarm_control.run()
