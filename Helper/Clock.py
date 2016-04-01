from time import time, timezone, strftime, localtime


class Clock:

    def __init__(self):
        self.offset = 0
        self.starttime = None

    def SetOffset(self, seconds):
        self.offset = seconds

    def ResetOffsetToLocal(self):
        self.offset = timezone

    def GetEpoch(self):
        return time()

    def TimerStart(self):
        self.starttime = self.GetEpoch()

    def TimerGet(self):
        starttime = self.starttime
        if not starttime:
            raise Exception("Timer not started.")
        stoptime = self.GetEpoch()
        dif = stoptime - starttime
        dif = "%.2f" % dif
        return dif

    def EpochToStr(self, epoch):
        return strftime('%Y-%m-%d %H:%M:%S', localtime(epoch))
