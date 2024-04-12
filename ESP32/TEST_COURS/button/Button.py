from machine import Pin
import time
from Tester import Testable

class Button(Testable):
    def __init__(self, nb, delegate) -> None:
        self.pin = Pin(nb, Pin.IN, Pin.PULL_DOWN)
        self.isPressed = False
        self.delegate = delegate
        self.time_ms_error = 10000
    
    def process(self):
        if self.pin.value() != self.isPressed:
            self.isPressed = not self.isPressed
            self.delegate.change_click(self.isPressed)

    def test(self):
        actual_time_ms = 0
        while actual_time_ms < self.time_ms_error:
            time.sleep(0.05)
            actual_time_ms += 50
            if self.pin.value() == 1:
                self.isPressed = True
                return True
        return False
