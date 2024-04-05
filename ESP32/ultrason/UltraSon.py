from machine import Pin
from Tester import Testable
import time

class PinUltraSon(Testable):
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

    def test(self, time_ms_error):
        actual_time_ms = 0
        isSending = False
        isSended = False
        isReceiving = False
        isReceived = False

        while actual_time_ms < time_ms_error:
            time.sleep(0.001)
            actual_time_ms += 1
            if not isSending and not isSended:
                self.trig.value(1)
                isSending = True
            elif isSending and not isSended:
                self.trig.value(0)
                isSended = True
            elif not isReceiving and not isReceived:
                if self.echo.value() != 0:
                    isReceiving = True
            elif isReceiving and not isReceived:
                if self.echo.value() != 1:
                    isReceived = True
            if isReceived:
                return True
        return False


class UltraSon(Testable):
    def __init__(self, trig, echo, delegate) -> None:
        self.pin = PinUltraSon(trig, echo)
        self.isGoodDistance = False
        self.delegate = delegate
        self.time_ms_error = 500

    def process(self):
        self.pin.process()
        pulse_duration = time.ticks_diff(self.pin.pulse_end, self.pin.pulse_start)
        distance = distance = (pulse_duration * 0.0343) / 2
        distance = round(distance, 2)

        if distance < 10 and not self.isGoodDistance:
            self.isGoodDistance = True
            self.delegate.good_distance()
        elif distance > 10 and self.isGoodDistance:
            self.isGoodDistance = False
            self.delegate.bad_distance()

    def test(self):
        return self.pin.test(self.time_ms_error)

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
