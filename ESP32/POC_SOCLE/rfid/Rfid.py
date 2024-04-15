from Tester import Testable
from threading import Thread
import time, random
from mfrc522 import SimpleMFRC522


class Rfid(Thread, Testable):
    def __init__(self, delegate) -> None:
        super().__init__()
        self.delegate = delegate
        self.lastTimeDetected = 0
        self.reader = SimpleMFRC522()

    def run(self):
        try: 
            while True:
                id, text = self.reader.read()
                if id and self.delegate:
                    self.delegate.rfid_detected(str(id))
        except KeyboardInterrupt:
            pass

    def process(self):
        id = self.reader.read_id_no_block()
        if id and self.delegate:
                    self.delegate.rfid_detected(str(id))
                    
    def test(self):
        return True