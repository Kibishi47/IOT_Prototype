from Tester import Testable
import time, random

class Rfid(Testable):
    def __init__(self, delegate) -> None:
        self.delegate = delegate
        self.lastTimeDetected = 0
        self.id_test = [
            '1234',
            '5678'
        ]

    def process(self):
        actual_time = time.ticks_ms()
        if actual_time > self.lastTimeDetected + 5000:
            self.delegate.rfid_detected(random.choice(self.id_test))

    def test(self):
        return True