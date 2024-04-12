from time import sleep_ms

from button.SpecialButton import Button

from Callback import *
from wireless_manager import *
from Tester import TestLauncher

from DisplayError import DisplayError

PIN_BUTTON = 33

wirelessManager = WirelessManager(BLECallback("Manu"),WebsocketCallback())
button = Button(PIN_BUTTON, ClickButtonCallback(wirelessManager))

# TESTS
objects_to_test = [
    wirelessManager,
    button,
]
testLauncher = TestLauncher.debug_mode()
if testLauncher.test_objects(objects_to_test):
    try:
        # RUN
        while True:
            button.process()
            wirelessManager.process()
            sleep_ms(50)

    except KeyboardInterrupt:
        pass
else:
    try:
        DisplayError.print_error(testLauncher.get_class_name())
    except KeyboardInterrupt:
        pass
