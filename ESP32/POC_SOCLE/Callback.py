from button.ButtonDelegate import ButtonDelegate
from rfid.RfidDelegate import RfidDelegate
from wireless_manager import CommunicationCallback

class BLECallback(CommunicationCallback):

    def __init__(self,bleName="Default"):
        self.bleName = bleName
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
    

class WebsocketCallback(CommunicationCallback):

    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")

class ClickButtonCallback(ButtonDelegate):
    def __init__(self, wirelessManager) -> None:
        super().__init__()
        self.wirelessManager = wirelessManager

    def short_click(self):
        print("short_click")

    def long_click(self):
        print("long_click")

class RfidCallback(RfidDelegate):
    def __init__(self, wirelessManager) -> None:
        super().__init__()
        self.wirelessManager = wirelessManager

    def rfid_detected(self, rfid_id):
        self.wirelessManager.sendDataToWS(rfid_id)