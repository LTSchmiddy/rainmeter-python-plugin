# A Control Module for RmPython to help manage module imports and other interpreter tasks:

import sys, os, importlib

class ModuleLoader:
    
    def setup(self, rm, *args):
        # return args
        rm.RmLog(rm.LOG_NOTICE, str(rm))