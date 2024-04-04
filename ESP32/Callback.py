from button.Button import Button
from button.ButtonDelegate import ButtonDelegate

from accelerometer.AccelGyro import AccelGyro
from accelerometer.AccelGyroDelegate import AccelGyroDelegate

from ultrason.UltraSon import UltraSon
from ultrason.UltraSonDelegate import UltraSonDelegate

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


class DirectionCallBack(AccelGyroDelegate):
    def __init__(self, wirelessManager) -> None:
        super().__init__()
        self.wirelessManager = wirelessManager

    def left(self):
        super().left()
        self.wirelessManager.sendDataToWS("d:GAUCHE")
    
    def right(self):
        super().right()
        self.wirelessManager.sendDataToWS("d:DROITE")

class ChangeClickButtonCallback(ButtonDelegate):
    def __init__(self, wirelessManager) -> None:
        super().__init__()
        self.wirelessManager = wirelessManager

    def change_click(self, isPressed):
        if isPressed:
            message = "pressed"
        else:
            message = "not-pressed"
        print(message)
        self.wirelessManager.sendDataToWS("b:" + message)

class DistanceCallback(UltraSonDelegate):
    def __init__(self, wirelessManager) -> None:
        super().__init__()
        self.wirelessManager = wirelessManager

    def good_distance(self):
        super().good_distance()
        self.wirelessManager.sendDataToWS("u:true")

    def bad_distance(self):
        super().bad_distance()
        self.wirelessManager.sendDataToWS("u:false")