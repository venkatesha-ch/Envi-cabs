class Driver:
    def __init__(self, id, timeNextAvl, currentLoc = "unknown"):
        self.id = id
        self.currentLoc = currentLoc
        self.timeNextAvl = timeNextAvl
    
class Booking:
    def __init__(self, id, origin, dest, sTime, rTime, reqDrive = 1):
        self.id = id
        self.origin = origin
        self.dest = dest
        self.sTime = sTime
        self.timeReq = rTime
        self.requiredDrive = reqDrive

class TimeEstimate:
    def __init__(self, source, dest, reqTime):
        self.source = source
        self.dest = dest
        self.reqTime = reqTime
