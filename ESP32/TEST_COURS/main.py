from time import sleep_ms

from button.Button import Button
from accelerometer.AccelGyro import AccelGyro
from ultrason.UltraSon import UltraSon

from Callback import *
from wireless_manager import *
from Tester import TestLauncher

from DisplayError import DisplayError

PIN_BUTTON = 33
PIN_SCL = 22
PIN_SDA = 21
PIN_TRIG = 14
PIN_ECHO = 12

isRunnable = True

wirelessManager = WirelessManager(BLECallback("Manu"),WebsocketCallback())
button = Button(PIN_BUTTON, ClickButtonCallback(wirelessManager))

# INIT ACCELEROMETER AND ULTRASON
try:
    ag = AccelGyro(PIN_SCL, PIN_SDA, DirectionCallBack(wirelessManager))
except:
    isRunnable = False
    try:
        DisplayError.print_error(AccelGyro.__name__)
    except KeyboardInterrupt:
        pass
try:
    us = UltraSon(PIN_TRIG, PIN_ECHO, DistanceCallback(wirelessManager))
except:
    isRunnable = False
    try:
        DisplayError.print_error(UltraSon.__name__)
    except KeyboardInterrupt:
        pass

if isRunnable:
    # TESTS
    objects_to_test = [
        button,
        ag,
        us,
        wirelessManager,
    ]
    testLauncher = TestLauncher.debug_mode()
    if testLauncher.test_objects(objects_to_test):
        try:
            # RUN
            while True:
                button.process()
                ag.process()
                us.process()
                wirelessManager.process()
                sleep_ms(50)

        except KeyboardInterrupt:
            pass
    else:
        try:
            DisplayError.print_error(testLauncher.get_class_name())
        except KeyboardInterrupt:
            pass
