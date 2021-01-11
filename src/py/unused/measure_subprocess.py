import sys, os, subprocess, pickle

from PythonLoaderUtils.meaure_type import MeasureBase

class SubprocessMeasure(MeasureBase):
    proc: subprocess.Popen
    
    def __init__(self):
        self.var = "hello"
        
    def Reload(self, rm, maxValue):
        pass

    def Update(self):
        return 1.0

    def GetString(self):
        return ''

    def ExecuteBang(self, args):
        pass

    def Finalize(self):
        pass

