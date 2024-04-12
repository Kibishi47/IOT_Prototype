from accelerometer.mpu6050 import accel
from Tester import Testable
from machine import I2C, Pin
import time

class CalculDirection:
    def __init__(self) -> None:
        self.samples = []
        self.max_sample = 500

        self.deltaX = 6000
        self.deltaTime = 400

        self.last_time_movement = 0
        self.canMove = True
    
    def calcul_direction(self, data):
        actual_time = time.ticks_ms()
        self.samples.append(data["AcY"])
        if len(self.samples) > self.max_sample:
            self.samples.pop(0)
        center = sum(self.samples) / len(self.samples)
        center = 0

        if data["AcY"] > center + self.deltaX and self.canMove:
            self.canMove = False
            self.last_time_movement = actual_time
            direction = "DROITE"
        elif data["AcY"] < center - self.deltaX and self.canMove:
            self.canMove = False
            self.last_time_movement = actual_time
            direction = "GAUCHE"
        else:
            direction = "MIDDLE"
        
        if actual_time > self.last_time_movement + self.deltaTime:
            self.canMove = True

        return direction


class AccelGyro(Testable):
    def __init__(self, scl, sda, delegate) -> None:
        i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        self.mpu= accel(i2c)
        self.calculator = CalculDirection()
        self.delegate = delegate
        self.time_ms_error = 1000
        self.margin_error = 10

    def process(self):
        data = self.mpu.get_values()
        direction = self.calculator.calcul_direction(data)
        if direction == "GAUCHE":
            self.delegate.left()
        elif direction == "DROITE":
            self.delegate.right()

    def test(self):
        actual_time_ms = 0
        keys = ['GyZ', 'GyY', 'GyX', 'AcZ', 'AcY', 'AcX']
        keys_number = 6
        last_values = None
        variation_number = 0
        while actual_time_ms < self.time_ms_error:
            time.sleep(0.05)
            actual_time_ms += 50
            data = self.mpu.get_values()
            if data != last_values:
                variation_number += 1
            last_values = data
            if variation_number >= (self.time_ms_error / 50) / 2:
                return True

            bad_keys = []
            for key in keys:
                if data[key] == 0:
                    bad_keys.append(key)
            if len(bad_keys) == keys_number:
                return False
        return False
    
        