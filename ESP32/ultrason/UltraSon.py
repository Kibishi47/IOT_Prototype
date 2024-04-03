from machine import Pin
import time

class GPIOUltraSon:
    def __init__(self, trig, echo) -> None:
        self.trig = Pin(trig, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)
        self.pulse_start = 0
        self.pulse_end = 0

    def process(self):
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)
        while self.echo.value() == 0:
            self.pulse_start = time.ticks_us()

        while self.echo.value() == 1:
            self.pulse_end = time.ticks_us()

class UltraSon(GPIOUltraSon):
    def __init__(self, trig, echo, delegate) -> None:
        super().__init__(trig, echo)
        self.isGoodDistance = False
        self.delegate = delegate

    def process(self):
        super().process()
        pulse_duration = time.ticks_diff(self.pulse_end, self.pulse_start)
        distance = distance = (pulse_duration * 0.0343) / 2
        distance = round(distance, 2)

        if distance < 10 and not self.isGoodDistance:
            self.isGoodDistance = True
            self.delegate.good_distance()
        elif distance > 10 and self.isGoodDistance:
            self.isGoodDistance = False
            self.delegate.bad_distance()

TRIG = 23
ECHO = 24

def printDistance(distance):
    print(f"Distance: {distance}cm")

if __name__ == "__main__":
    try:
        us = UltraSon(TRIG, ECHO, printDistance)
        while True:
            us.process()
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Mesure arrêtée par l'utilisateur")
