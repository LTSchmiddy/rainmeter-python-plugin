import sys, pickle, os


class MeasureBase:
    def __init__(self):
        self.var = "hello"

    def Reload(self, rm, maxValue):
        pass

    def Update(self):
        return 1.0

    def GetString(self):
        return ""

    def ExecuteBang(self, args):
        pass

    def Finalize(self):
        pass
