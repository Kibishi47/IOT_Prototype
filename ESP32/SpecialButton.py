from machine import Pin
import time

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
        self.longClickDelta = 1000
        self.clickedTimes = [0] * 4

    def checkIsDoubleClick(self, numberOfTheChangement):
        self.clickedTimes[numberOfTheChangement] = time.ticks_ms()
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
            return not time.ticks_ms() <= maxTime
        return True
    
    def resetClickedTimes(self):
        self.clickedTimes = [0] * 4

class Button:
    def __init__(self, nb, debug = False, detectionMode = DetectionMode.LONG_CLICK) -> None:
        self.pin = Pin(nb, Pin.IN, Pin.PULL_DOWN)
        self.isPressed = False
        self.numberOfTheChangement = -1
        self.calcul = CalculButton()
        self.debug = debug
        self.lastTimePressed = None
        self.lastTimeUnpressed = None
        self.clickHistory = []
        self.detectionMode = detectionMode

    def process(self):
        self.checkChangement()
        

    def checkChangement(self):
        if self.pin.value() != self.isPressed:
            self.isPressed = not self.isPressed
            self.hasChange()
            

    def hasChange(self):
        changeTime = time.ticks_ms()
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
            if not self.isPressed:
                isLongClick = self.calcul.checkIsLongClick(self.lastTimePressed)
        if self.debug:
            print(self.calcul.clickedTimes)
        if isLongClick == False or isDoubleClick == False:
            print("\nShort click")
            self.lastTimeClick = changeTime
            self.clickHistory.append(0)
            self.resetClick()
            if self.isPressed:
                self.hasChange()
        elif isDoubleClick == True:
            print("\nDouble click")
            self.lastTimeClick = changeTime
            self.clickHistory.append(0)
            self.clickHistory.append(0)
            self.resetClick()
        elif isLongClick == True:
            print("\nLong click")
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