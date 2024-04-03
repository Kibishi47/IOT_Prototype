from time import sleep_ms
from wireless_manager import *

from button.Button import Button
from button.ButtonDelegate import ButtonDelegate

from accelerometer.AccelGyro import AccelGyro
from accelerometer.AccelGyroDelegate import AccelGyroDelegate

from ultrason.UltraSon import UltraSon
from ultrason.UltraSonDelegate import UltraSonDelegate


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
    def __init__(self) -> None:
        super().__init__()

    def left(self):
        super().left()
        wirelessManager.sendDataToWS("d:GAUCHE")
    
    def right(self):
        super().right()
        wirelessManager.sendDataToWS("d:DROITE")

class ChangeClickButtonCallback(ButtonDelegate):
    def __init__(self) -> None:
        super().__init__()

    def change_click(self, isPressed):
        if isPressed:
            message = "pressed"
        else:
            message = "not-pressed"
        print(message)
        wirelessManager.sendDataToWS("b:" + message)

class DistanceCallback(UltraSonDelegate):
    def __init__(self) -> None:
        super().__init__()

    def good_distance(self):
        super().good_distance()
        wirelessManager.sendDataToWS("u:true")

    def bad_distance(self):
        super().bad_distance()
        wirelessManager.sendDataToWS("u:false")


PIN_BUTTON = 33
PIN_SCL = 22
PIN_SDA = 21
PIN_TRIG = 14
PIN_ECHO = 12

wirelessManager = WirelessManager(BLECallback("Manu"),WebsocketCallback())
ag = AccelGyro(PIN_SCL, PIN_SDA, DirectionCallBack())
button = Button(PIN_BUTTON, ChangeClickButtonCallback())
us = UltraSon(PIN_TRIG, PIN_ECHO, DistanceCallback())

try:
    while True:
        wirelessManager.process()
        us.process()
        ag.process()
        button.process()
        sleep_ms(50)

except KeyboardInterrupt:
    pass
