""" 
NO ERROR: No flashing
WIRELESS MANAGER // WEB SOCKET CLIENT ERROR: Single flash
BUTTON ERROR: Double flash
ACCELEROMETER ERROR: Triple flash
ULTRASON ERROR: Quadruple flash
RFID ERROR: Pentuple flash

ALL SPACE BY 1 SECOND
"""

import time

class ErrorType:
    WIRELESSMANAGER = "WirelessManager"
    BUTTON = "Button"
    ACCELEROMETER = "AccelGyro"
    ULTRASON = "UltraSon"

    DICT = {
        "WirelessManager": 1,
        "WebSocketClient": 1,
        "Button": 2,
        "AccelGyro": 3,
        "UltraSon": 4,
        "Rfid": 5
    }

class DisplayError:
    def __init__(self) -> None:
        pass

    @staticmethod
    def print_error(class_name):
        if class_name in ErrorType.DICT:
            print(f"There is an error for: {class_name}")
        else:
            print("No class name known for this error")