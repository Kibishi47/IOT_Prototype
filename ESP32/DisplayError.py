""" 
NO ERROR: No flashing
WIRELESS MANAGER ERROR: Single flash
BUTTON ERROR: Double flash
ACCELEROMETER ERROR: Triple flash
ULTRASON ERROR: Quadruple flash

ALL SPACE BY 1 SECOND
"""

from time import sleep_ms

class ErrorType:
    WIRELESSMANAGER = "WirelessManager"
    BUTTON = "Button"
    ACCELEROMETER = "AccelGyro"
    ULTRASON = "UltraSon"

    DICT = {
        "WirelessManager": 1,
        "Button": 2,
        "AccelGyro": 3,
        "UltraSon": 4
    }

class DisplayError:
    def __init__(self) -> None:
        pass

    def print_error(self, class_name):
        if class_name in ErrorType.DICT:
            self.print_x_time(ErrorType.DICT[class_name])
        else:
            return False
        return True

    def print_x_time(self, number_of_print):
        for i in range(0, number_of_print):
            sleep_ms(300)
            print("")