from accelerometer.mpu6050 import accel
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


class AccelGyro:
    def __init__(self, scl, sda, delegate) -> None:
        i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        self.mpu= accel(i2c)
        self.calculator = CalculDirection()
        self.delegate = delegate

    def process(self):
        data = self.mpu.get_values()
        direction = self.calculator.calcul_direction(data)
        if direction == "GAUCHE":
            self.delegate.left()
        elif direction == "DROITE":
            self.delegate.right()
        