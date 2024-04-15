import RPi.GPIO as GPIO
import time
from Tester import Testable

class DetectionMode:
    LONG_CLICK = 0
    DOUBLE_CLICK = 1
    DOUBLE_AND_LONG_CLICK = 2

class CalculButton:
    def __init__(self) -> None:
        self.doubleClickDeltas = [
            300, # Delta 1
            90 # Delta 2
        ]
        self.longClickDelta = 750
        self.clickedTimes = [0] * 4

    def checkIsDoubleClick(self, numberOfTheChangement):
        self.clickedTimes[numberOfTheChangement] = time.time() * 1000
        if numberOfTheChangement == 0:
            return None
        if numberOfTheChangement == 1:
            if self.checkIsInDoubleClickDelta1(numberOfTheChangement):
                return None
            else:
                return False
        if numberOfTheChangement == 2:
            if self.checkIsInDoubleClickDelta2(numberOfTheChangement) and self.checkIsInDoubleClickDelta1(numberOfTheChangement):
                return None
            else:
                return False
        if numberOfTheChangement == 3:
            if self.checkIsInDoubleClickDelta1(numberOfTheChangement):
                return True
            else:
                return False
        return None

    def checkIsInDoubleClickDelta1(self, numberOfTheChangement):
        if len(self.clickedTimes) >= 1:
            maxTime = self.clickedTimes[0] + self.doubleClickDeltas[0]
            return self.clickedTimes[numberOfTheChangement] <= maxTime
        return False
    
    def checkIsInDoubleClickDelta2(self, numberOfTheChangement):
        if len(self.clickedTimes) > 1:
            maxTime = self.clickedTimes[1] + self.doubleClickDeltas[1]
            return self.clickedTimes[numberOfTheChangement] <= maxTime
        return False
    
    def checkIsLongClick(self, lastTimeClick):
        if len(self.clickedTimes) > 1:
            maxTime = lastTimeClick + self.longClickDelta
            return not time.time() * 1000 <= maxTime
        return True
    
    def resetClickedTimes(self):
        self.clickedTimes = [0] * 4


class Button(Testable):
    def __init__(self, nb, delegate, debug = False, detectionMode = DetectionMode.LONG_CLICK) -> None:
        self.nb = nb
        self.isPressed = False
        self.numberOfTheChangement = -1
        self.calcul = CalculButton()
        self.debug = debug
        self.lastTimePressed = None
        self.lastTimeUnpressed = None
        self.clickHistory = []
        self.detectionMode = detectionMode
        self.delegate = delegate
        self.time_ms_error = 10000
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.nb, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def process(self):
        self.checkChangement()
        

    def checkChangement(self):
        status = GPIO.input(self.nb) == GPIO.HIGH
        if status != self.isPressed:
            self.isPressed = not self.isPressed
            self.hasChange()
            

    def hasChange(self):
        changeTime = time.time() * 1000
        self.numberOfTheChangement += 1
        isDoubleClick = None
        isLongClick = None
        if self.isPressed:
            self.lastTimePressed = changeTime
        else:
            self.lastTimeUnpressed = changeTime
        if self.detectionMode == DetectionMode.DOUBLE_CLICK or self.detectionMode == DetectionMode.DOUBLE_AND_LONG_CLICK:
            isDoubleClick = self.calcul.checkIsDoubleClick(self.numberOfTheChangement)
        if self.detectionMode == DetectionMode.LONG_CLICK or self.detectionMode == DetectionMode.DOUBLE_AND_LONG_CLICK:
            if not self.isPressed and self.lastTimePressed is not None:
                isLongClick = self.calcul.checkIsLongClick(self.lastTimePressed)
        if self.debug:
            print(self.calcul.clickedTimes)
        if isLongClick == False or isDoubleClick == False: # SHORT_CLICK
            if self.delegate is not None:
                self.delegate.short_click()
            self.lastTimeClick = changeTime
            self.clickHistory.append(0)
            self.resetClick()
            if self.isPressed:
                self.hasChange()
        elif isDoubleClick == True: # DOUBLE CLICK
            if self.delegate is not None:
                self.delegate.double_click()
            self.lastTimeClick = changeTime
            self.clickHistory.append(0)
            self.clickHistory.append(0)
            self.resetClick()
        elif isLongClick == True: # LONG CLICK
            if self.delegate is not None:
                self.delegate.long_click()
            self.lastTimeClick = changeTime
            self.clickHistory.append(1)
            self.resetClick()
            if self.isPressed:
                self.hasChange()

    def resetClick(self):
        self.numberOfTheChangement = -1
        self.calcul.resetClickedTimes()
        if self.debug:
            print(f"Reset: {self.calcul.clickedTimes}")

    def test(self):
        actual_time_ms = 0
        while actual_time_ms < self.time_ms_error:
            time.sleep(0.05)
            actual_time_ms += 50
            if GPIO.input(self.nb) == GPIO.HIGH:
                self.isPressed = True
                return True
        return False