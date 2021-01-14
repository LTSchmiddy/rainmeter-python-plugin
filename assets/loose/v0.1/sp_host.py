# A Control Module for RmPython to help manage module imports and other interpreter tasks:
from __future__ import annotations
import sys, os, pathlib, traceback

from PythonLoaderUtils.stdhandler import StdHandler
from PythonLoaderUtils.meaure_type import MeasureBase
from PythonLoaderUtils.module_handler import ModuleHandler
from PythonLoaderUtils.module_info import ModuleInfo
from PythonLoaderUtils.rm_stub import RainmeterW

from PythonLoaderUtils import pip_handler

# import subinterp
from subinterp import SubInterp

instance: SpHost = None


class MeasureRef:
    siKey: str
    mId: int

    def __init__(self, mId: int, siKey: str = "__main__"):
        self.mId = mId
        self.siKey = siKey


class CountingSubInterp(SubInterp):
    num_measures: int = 0


class SpHost:
    _instance: SpHost

    out: StdHandler
    err: StdHandler

    # si: SubInterp

    mod_si: dict[str, SubInterp]

    exec_path: str
    console_exec_path: str

    last_rm: RainmeterW

    @classmethod
    def get_instance(cls) -> SpHost:
        return cls._instance

    @classmethod
    def set_instance(cls, p_instance: SpHost) -> SpHost:
        global instance
        cls._instance = p_instance
        instance = p_instance

    def _setup_stdout(self, rm: RainmeterW):
        self.out = StdHandler("Py", rm, rm.LOG_NOTICE)
        self.err = StdHandler("PyErr", rm, rm.LOG_ERROR)

        # Just in case:
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr

        sys.stdout = self.out
        sys.stderr = self.err

    def setup(self, rm, exec_path: str, console_exec_path: str = ""):
        self.set_instance(self)
        self._setup_stdout(rm)

        self.last_rm = rm

        print("Starting Python subprocess...")
        print(sys.path)

        self.exec_path = exec_path
        self.console_exec_path = console_exec_path
        
        pip_handler.interp_path = console_exec_path
        
        print(f"{self.exec_path=}")
        print(f"{self.console_exec_path=}")

        CountingSubInterp.set_interp_path(self.exec_path)
        ModuleInfo.set_interp_path(self.console_exec_path)
        self.mod_si = {}

        if not pip_handler.check_for_pip():
            pip_handler.install_pip()
        # self.si = self.newInterpreter()

        # print(f"returned {self.sp_request(rm, {})}")

    def sp_request(self, request: dict, interp: CountingSubInterp = None):
        if interp is None:
            interp = self.si

        return interp.exchange(self.last_rm, request)

    def setRm(self, rm):
        self.last_rm = rm

        self.out.rm = rm
        self.err.rm = rm

    def newInterpreter(self, siKey="__main__"):
        print(f"Starting interpreter for '{siKey}'...")        
        cpath = os.path.abspath("sp_child.py")
        print(f"{cpath=}")
        retVal = CountingSubInterp(str(cpath), "spChildMain", "sp_child_")
        self.mod_si[siKey] = retVal
        return retVal
    
    def newInterpreter_Info(self, minfo: ModuleInfo):
        print(f"Starting interpreter for '{minfo.active_siKey}'...")
        
        if minfo.should_setup_run:
            pip_handler.setup_minfo(minfo)
        
        cpath = os.path.abspath("sp_child.py")
        print(f"{cpath=}")
        
        retVal = CountingSubInterp(
            str(cpath),
            "spChildMain", 
            "sp_child_", 
            popen_args = {
                'cwd': minfo.abs_working_directory
            }, 
            use_interp_path=minfo.abs_venv_exec
        )
        
        minfo.save_module_info()
        
        self.mod_si[minfo.active_siKey] = retVal
        return retVal
    
    def destroyInterpreter(self, siKey="__main__"):
        self.sp_request({"type": "exit"}, self.mod_si[siKey])
        
        self.mod_si[siKey].proc.wait()
        del self.mod_si[siKey]

    def getInterpreter(self, siKey: str, info_mode: bool = False) -> CountingSubInterp:
        minfo = None
        if info_mode:
            minfo = ModuleInfo.load_module_info(siKey)
            siKey = minfo.active_siKey
        
        if siKey in self.mod_si.keys():
            return self.mod_si[siKey]

        else:
            if info_mode:
                return self.newInterpreter_Info(minfo)
            else:
                return self.newInterpreter(siKey)

    # If loadMeasure returns None, then the measure was unable to be loaded by the subprocess.
    # In this case, check the subprocess log file.
    def loadMeasure(self, rm: RainmeterW = None):
        self.setRm(rm)

        interp = None
        siKey = None

        if rm.RmReadPath("Info", "") != "":
            siKey, interp = self.loadInterp_Info(rm)
        
        elif rm.RmReadPath("Path", "") != "":
            siKey, interp = self.loadInterp_Path(rm)

        elif rm.RmReadString("Module", "") != "":
            siKey, interp = self.loadInterp_Module(rm)

        mId = self.sp_request({"type": "loadMeasure"}, interp)

        if mId is None:
            rm.RmLog(
                rm.LOG_ERROR,
                "This measure could not be loaded. Check the sub-process log file for details.",
            )
        # else:
        #     print(mId)

        interp.num_measures += 1
        return MeasureRef(mId, siKey)

    def loadInterp_Module(self, rm: RainmeterW):
        return ('__main__', self.getInterpreter('__main__'))
    
    def loadInterp_Path(self, rm: RainmeterW):
        return ('__main__', self.getInterpreter('__main__'))
    
    def loadInterp_Info(self, rm: RainmeterW):
        siKey = str(pathlib.Path( rm.RmReadPath("Info", "")).resolve())
        interp = self.getInterpreter(siKey, True)
        
        return (siKey, interp)
    
    
    # Wrappers for measure calls. Used to catch errors and print them to the log.
    def callReload(self, m: MeasureRef, rm, maxValue: float):
        if m.mId is None:
            return

        self.setRm(rm)

        try:
            return self.sp_request(
                {"type": "callReload", "mId": m.mId, "maxValue": maxValue},
                self.getInterpreter(m.siKey),
            )
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)

    def callUpdate(self, m: MeasureRef):
        if m.mId is None:
            return 1.0

        try:
            return self.sp_request(
                {"type": "callUpdate", "mId": m.mId}, self.getInterpreter(m.siKey)
            )
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)
            return 1.0

    def callGetString(self, m: MeasureRef):
        if m.mId is None:
            return "ERROR: Could not load Measure."

        try:
            return self.sp_request(
                {"type": "callGetString", "mId": m.mId}, self.getInterpreter(m.siKey)
            )
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)
            return "ERROR: {e}"

    def callExecuteBang(self, m: MeasureRef, args):
        if m.mId is None:
            return

        try:
            return self.sp_request(
                {"type": "callExecuteBang", "mId": m.mId, "args": args},
                self.getInterpreter(m.siKey),
            )
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)

    def callFinalize(self, m: MeasureRef):
        if m.mId is None:
            return

        interp = self.getInterpreter(m.siKey)
        
        try:
            retVal = self.sp_request(
                {
                    "type": "callFinalize",
                    "mId": m.mId,
                },
                interp,
            )
            interp.num_measures -= 1
            
            if interp.num_measures == 0:
                self.destroyInterpreter(m.siKey)
            
            if interp.num_measures < 0:
                raise Exception(f"interp.num_measures should never be less than zero, but {interp.num_measures=}")
            
            return retVal
            
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)

    def callFunc(self, m: MeasureRef, fname: str, args: tuple):
        if m.mId is None:
            return "ERROR: Could not load measure."

        try:
            # return "HI"
            return str(
                self.sp_request(
                    {"type": "callFunc", "mId": m.mId, "fname": fname, "args": args},
                    self.getInterpreter(m.siKey),
                )
            )
        except Exception as e:
            # self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            traceback.print_exception(type(e), e, e.__traceback__)
            return None

    def terminate(self):        
        print("All sub-interpreters terminated.")
        # self.si.proc.terminate()
