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

    @staticmethod
    def print_error(class_name, time_ms_printing_error = 20000):
        actual_time_ms = 0
        number_of_print = 1
        while actual_time_ms < time_ms_printing_error:
            if class_name in ErrorType.DICT:
                number_of_print = ErrorType.DICT[class_name]
                DisplayError.print_x_time(number_of_print)
                sleep_ms(1000)
                actual_time_ms += 1000 + 300*number_of_print
            else:
                print("")

    @staticmethod
    def print_x_time(number_of_print):
        for i in range(0, number_of_print):
            sleep_ms(300)
            print("")