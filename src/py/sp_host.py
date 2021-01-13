# A Control Module for RmPython to help manage module imports and other interpreter tasks:
from __future__ import annotations
import sys, os, json, pathlib

from PythonLoaderUtils.stdhandler import StdHandler
from PythonLoaderUtils.meaure_type import MeasureBase
from PythonLoaderUtils.module_handler import ModuleHandler
from PythonLoaderUtils.module_info import ModuleInfo
from PythonLoaderUtils.pip_handler import check_for_pip
from PythonLoaderUtils.rm_stub import RainmeterW

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
    mun_measures: int = 0


class SpHost:
    _instance: SpHost

    out: StdHandler
    err: StdHandler

    si: SubInterp

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
        self.err = StdHandler("Py", rm, rm.LOG_ERROR)

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
        print(f"{self.exec_path=}")
        print(f"{self.console_exec_path=}")

        CountingSubInterp.set_interp_path(self.exec_path)
        ModuleInfo.set_interp_path(self.console_exec_path)
        self.mod_si = {}

        check_for_pip()
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

    def newInterpreter(self, info_path="__main__"):
        print(f"Starting interpreter for '{info_path}'...")
        
        
        use_interp = None
        if info_path != "__main__":
            minfo = ModuleInfo.load_module_info(info_path)
            minfo.run_setup()
            use_interp = minfo.abs_venv_exec
        
        cpath = os.path.abspath("sp_child.py")
        print(f"{cpath=}")
        retVal = CountingSubInterp(str(cpath), "spChildMain", "sp_child_", use_interp_path=use_interp)
        self.mod_si[info_path] = retVal
        return retVal

    def getInterpreter(self, info_path: str) -> CountingSubInterp:
        # minfo = ModuleInfo.load_module_info(info_path)

        if info_path in self.mod_si.keys():
            return self.mod_si[info_path]

        else:
            return self.newInterpreter(info_path)

    # If loadMeasure returns None, then the measure was unable to be loaded by the subprocess.
    # In this case, check the subprocess log file.
    def loadMeasure(self, rm: RainmeterW = None):
        self.setRm(rm)

        interp = None

        # siKey = str(pathlib.Path(rm.RmReadPath("Info", "")).resolve())
        siKey = rm.RmReadPath("Info", "")
        print(f"{siKey=}")

        if len(siKey) > 0:
            siKey = str(pathlib.Path(siKey).resolve())
            interp = self.getInterpreter(siKey)

        else:
            siKey = "__main__"
            interp = self.getInterpreter(siKey)

        mId = self.sp_request({"type": "loadMeasure"}, interp)

        if mId is None:
            rm.RmLog(
                rm.LOG_ERROR,
                "This measure could not be loaded. Check the sub-process log file for details.",
            )
        else:
            print(mId)

        return MeasureRef(mId, siKey)

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
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

    def callUpdate(self, m: MeasureRef):
        if m.mId is None:
            return 1.0

        try:
            return self.sp_request(
                {"type": "callUpdate", "mId": m.mId}, self.getInterpreter(m.siKey)
            )
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return 1.0

    def callGetString(self, m: MeasureRef):
        if m.mId is None:
            return "ERROR: Could not load Measure."

        try:
            return self.sp_request(
                {"type": "callGetString", "mId": m.mId}, self.getInterpreter(m.siKey)
            )
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
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
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

    def callFinalize(self, m: MeasureRef):
        if m.mId is None:
            return

        try:
            return self.sp_request(
                {
                    "type": "callFinalize",
                    "mId": m.mId,
                },
                self.getInterpreter(m.siKey),
            )
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

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
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return None

    def terminate(self):
        print("Terminating Python sub-process...")
        self.si.proc.terminate()
