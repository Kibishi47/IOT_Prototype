from machine import Pin

class Button:
    def __init__(self, nb, delegate) -> None:
        self.pin = Pin(nb, Pin.IN, Pin.PULL_DOWN)
        self.isPressed = False
        self.delegate = delegate
    
    def process(self):
        if self.pin.value() != self.isPressed:
            self.isPressed = not self.isPressed
            self.delegate.change_click(self.isPressed)