from time import sleep_ms
from Callback import *
from wireless_manager import *
from Tester import TestLauncher

PIN_BUTTON = 33
PIN_SCL = 22
PIN_SDA = 21
PIN_TRIG = 14
PIN_ECHO = 12

wirelessManager = WirelessManager(BLECallback("Manu"),WebsocketCallback())
button = Button(PIN_BUTTON, ChangeClickButtonCallback(wirelessManager))
ag = AccelGyro(PIN_SCL, PIN_SDA, DirectionCallBack(wirelessManager))
us = UltraSon(PIN_TRIG, PIN_ECHO, DistanceCallback(wirelessManager))

# TESTS
objects_to_test = [
    wirelessManager,
    button,
    ag,
    us,
]

print(TestLauncher.test_object(ag))

if TestLauncher.test_objects(objects_to_test):
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
    print("ERROR")
