import machine
import time

button_pin = 7
led_pin = 20

button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(led_pin, machine.Pin.OUT)
led.value(0)

led_state = 0
last_button_state = 1
clock_period = 0.05 #20 Hz

while True:
    current_button_state = button.value()

    if current_button_state != last_button_state:
        if current_button_state == 0:
            led_state = 1 - led_state
            led.value(led_state)
        last_button_state = current_button_state

    time.sleep(clock_period)