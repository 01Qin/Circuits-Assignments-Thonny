from machine import Pin
import time


class AlarmControl:
    def __init__(self, alarm_pin=9, button_pin=7, red_light_pin=22, siren_pin=20):
        self.alarm_input = Pin(alarm_pin, Pin.IN, Pin.PULL_UP)
        self.button_input = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.red_light = Pin(red_light_pin, Pin.OUT)
        self.siren = Pin(siren_pin, Pin.OUT)

        self.current_state = "off"
        self.button_pressed = False
        self.last_toggle_time = time.ticks_ms()
        self.last_button_time = time.ticks_ms()

        self.red_light.off()
        self.siren.off()

    def debounce_button(self):

        if self.button_input.value() == 0:  # Button is pressed
            if not self.button_pressed and time.ticks_diff(time.ticks_ms(), self.last_button_time) > 50:
                self.button_pressed = True
                self.last_button_time = time.ticks_ms()
                return True  # Valid button press detected
        else:
            self.button_pressed = False  # Reset when released
        return False

    def handle_idle(self):
        """Initial state: Both siren and red light are OFF."""
        if self.alarm_input.value() == 0:  # Alarm triggered
            self.current_state = "Alarm activated"
            self.red_light.on()
            self.siren.on()

    def handle_alarm_triggered(self):
        """Alarm is active: Wait for button press to acknowledge."""
        if self.debounce_button():
            self.current_state = "Alarm_ACK"
            self.siren.off()  # Turn siren OFF, start blinking red light
        elif self.alarm_input.value() == 1:
            self.current_state = "Waiting"
            self.siren.off()
            self.red_light.on()

    def handle_waiting_for_ack(self):
        """Alarm turned off before acknowledgment: Red light stays ON until button press."""
        if self.debounce_button():
            self.current_state = "off"
            self.red_light.off()

    def handle_alarm_acknowledged(self):
        """Alarm acknowledged but still active: Siren OFF, red light blinks."""
        if self.alarm_input.value() == 1:  # Alarm deactivated
            self.current_state = "off"
            self.red_light.off()
        else:
            if time.ticks_diff(time.ticks_ms(), self.last_toggle_time) > 500:
                self.red_light.toggle()
                self.last_toggle_time = time.ticks_ms()

    def update_system(self):
        getattr(self, f"handle_{self.current_state.lower()}")()

    def run(self):
        """Main loop to run the state machine."""
        while True:
            self.update_system()
            time.sleep(0.05)  # Short loop delay


alarm_controller = AlarmControl()
alarm_controller.run()
