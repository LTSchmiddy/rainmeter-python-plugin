import sys

from PythonLoaderUtils.rm_stub import RainmeterW

n_instances = 0

class Measure:
    def __init__(self):
        global n_instances
        n_instances += 1
    
    def Reload(self, rm: RainmeterW, maxValue: float):
        global n_instances
        # n_instances += 1
        

    def Update(self):
        return 1.0

    def GetString(self):
        return 'Test 1'

    def ExecuteBang(self, args):
        pass

    def Finalize(self):
        global n_instances
        n_instances -= 1
    
    def InstCount(self):
        global n_instances
        return f"Has {n_instances}"