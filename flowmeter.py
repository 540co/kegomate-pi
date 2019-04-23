import config
import time

class Flowmeter:

    name = None
    kegId = None
    loggedTime = None
    firstTickOfEvent = None
    lastTick = 0

    def __init__(self, name, kegId):
        self.name = name
        self.kegId = kegId

    def isEventComplete(self):
        retVal = False
        currentTime = time.time()
        if ((self.loggedTime != None) and ((currentTime - self.loggedTime) >= config.postEventTimeCheck)):
            retVal = True
        return retVal

    def processTick(self, tick):
        self.setLastTick(tick)
        if(self.firstTickOfEvent == None):
            self.firstTickOfEvent = tick

    def setLastTick(self, lastTick):
        self.lastTick = lastTick

    def resetTimer(self):
        self.loggedTime = time.time()

    def resetEvent(self):
        self.loggedTime = None
        self.firstTickOfEvent = self.lastTick
