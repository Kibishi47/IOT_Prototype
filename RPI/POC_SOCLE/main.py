import RPi.GPIO as GPIO
import time

from button.SpecialButton import Button
from rfid.Rfid import Rfid
from WebSocketClient import *

from Callback import *
from Tester import TestLauncher

from DisplayError import DisplayError
GPIO.setmode(GPIO.BCM)

PIN_BUTTON = 17
ws_client = WebSocketClient("ws://192.168.42.82:8080", WebsocketCallback())
rfid = Rfid(RfidCallback(ws_client))
button = Button(PIN_BUTTON, ClickButtonCallback(ws_client))
ws_client.start()

# TESTS
objects_to_test = [
    rfid,
    ws_client,
    button,
]
testLauncher = TestLauncher.debug_mode()
if testLauncher.test_objects(objects_to_test):
    try:
        # RUN
        while True:
            rfid.process()
            button.process()
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
else:
    try:
        DisplayError.print_error(testLauncher.get_class_name())
    except KeyboardInterrupt:
        pass
GPIO.cleanup()