import sys
class StdHandler2():
    def __init__(self, mode: str):
        pass
    
    def write(self, msg):
        pass
    
    def flush(self):
        pass


class Measure2:
    def Reload(self, rm, maxValue):
        rm.RmLog(rm.LOG_NOTICE, "Reload called")

    def Update(self):
        return 1.0

    def GetString(self):
        return 'Test 2'

    def ExecuteBang(self, args):
        pass

    def Finalize(self):
        pass