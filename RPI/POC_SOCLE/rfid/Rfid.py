from Tester import Testable
from mfrc522 import SimpleMFRC522


class Rfid(Testable):
    def __init__(self, delegate) -> None:
        super().__init__()
        self.delegate = delegate
        self.lastTimeDetected = 0
        self.reader = SimpleMFRC522()
        self.card_presence = False
        self.none_array = []

    def process(self):
        id = self.reader.read_id_no_block()
        if id:
            self.none_array = []
            if self.delegate and not self.card_presence:
                self.delegate.rfid_detected(str(id))
            self.card_presence = True
        else:
            self.none_array.append(None)
            if len(self.none_array) >= 2:
                self.none_array = []
                self.card_presence = False
                    
    def test(self):
        return True