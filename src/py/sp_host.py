# A Control Module for RmPython to help manage module imports and other interpreter tasks:
from __future__ import annotations
import sys, os, json

from PythonLoaderUtils.stdhandler import StdHandler
from PythonLoaderUtils.meaure_type import MeasureBase
from PythonLoaderUtils.module_handler import ModuleHandler
from PythonLoaderUtils.pip_handler import check_for_pip
from PythonLoaderUtils.rm_stub import RainmeterW

# import subinterp
from subinterp import SubInterp

instance: SpHost = None

class SpHost:
    _instance: SpHost
    
    out: StdHandler
    err: StdHandler
    
    si: SubInterp
    
    exec_path: str
    
    lastRm: RainmeterW
    
    @classmethod 
    def get_instance(cls)->SpHost:
        return cls._instance
    
    @classmethod 
    def set_instance(cls, p_instance: SpHost)->SpHost:
        global instance
        cls._instance = p_instance
        instance = p_instance
    
    def _setup_stdout(self, rm: RainmeterW):
        self.out = StdHandler("Py", rm, rm.LOG_NOTICE)
        self.err = StdHandler("Py", rm, rm.LOG_ERROR)
        
        # Just in case:
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        
        sys.stdout = self.out
        sys.stderr = self.err

    
    def setup(self, rm, exec_path: str):
        self.set_instance(self)
        self._setup_stdout(rm)
        
        self.lastRm = rm
        
        print ("Starting Python subprocess...")
        print(sys.path)
        
        self.exec_path = exec_path
        print(f"{self.exec_path=}")
        
        SubInterp.set_interp_path(self.exec_path)
        self.si = SubInterp(os.path.abspath("sp_child.py"), 'spChildMain', "sp_child_")

        check_for_pip()
        
        # print(f"returned {self.sp_request(rm, {})}")
    
    def sp_request(self, request: dict):
        return self.si.exchange(self.lastRm, request)
        
        
        
    def setRm(self, rm):
        self.lastRm = rm
        
        self.out.rm = rm
        self.err.rm = rm
    
    def loadMeasure(self, rm: RainmeterW = None):
        self.setRm(rm)
        
        mId = self.sp_request({
            'type': 'loadMeasure'
        })

        print(mId)
        return mId
    
    # Wrappers for measure calls. Used to catch errors and print them to the log.
    def callReload(self, m: int, rm, maxValue: float):
        self.setRm(rm)
        try:
            return self.sp_request({
                'type': 'callReload',
                'mId': m,
                'maxValue' : maxValue
            })
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
    
    def callUpdate(self, m: int):
        try:
            return self.sp_request({
                'type': 'callUpdate',
                'mId': m
            })
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return 1.0

    def callGetString(self, m: int):
        try:
            return self.sp_request({
                'type': 'callGetString',
                'mId': m
            })
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return "ERROR"

    def callExecuteBang(self, m: int, args):
        try:
            return self.sp_request({
                'type': 'callExecuteBang',
                'mId': m,
                'args': args
            })
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))


    def callFinalize(self, m: int):
        try:
            return self.sp_request({
                'type': 'callFinalize',
                'mId': m,
            })
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
                
    def callFunc(self, m: int, fname: str, args: tuple):
        try:
            # return "HI"
            return str(self.sp_request({
                'type': 'callFunc',
                'mId': m,
                'fname': fname,
                'args': args
            }))
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return None
    
    def terminate(self):
        print("Terminating Python sub-process...")
        self.si.proc.terminate()

