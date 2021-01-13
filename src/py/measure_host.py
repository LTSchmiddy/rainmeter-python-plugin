# A Control Module for RmPython to help manage module imports and other interpreter tasks:
from __future__ import annotations
import sys, os

import pickle

from PythonLoaderUtils.stdhandler import StdHandler
from PythonLoaderUtils.meaure_type import MeasureBase
from PythonLoaderUtils.module_handler import ModuleHandler
from PythonLoaderUtils.pip_handler import check_for_pip
from PythonLoaderUtils.rm_stub import RainmeterW

instance: MeasureHost = None


class MeasureHost:
    _instance: MeasureHost

    std_mode: bool

    out: StdHandler
    err: StdHandler

    mh: ModuleHandler

    exec_path: str
    console_exec_path: str

    @classmethod
    def get_instance(cls) -> MeasureHost:
        return cls._instance

    @classmethod
    def set_instance(cls, p_instance: MeasureHost) -> MeasureHost:
        global instance
        cls._instance = p_instance
        instance = p_instance

    def __init__(self, p_std_mode=True) -> None:
        super().__init__()
        self.std_mode = p_std_mode

    def _setup_stdout(self, rm: RainmeterW):
        self.out = StdHandler("Py", rm, rm.LOG_NOTICE)
        self.err = StdHandler("Py", rm, rm.LOG_ERROR)

        # Just in case:
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr

        sys.stdout = self.out
        sys.stderr = self.err

    def setup(self, rm, exec_path: str, console_exec_path: str = None):
        self.set_instance(self)

        if self.std_mode:
            self._setup_stdout(rm)

        print(sys.path)

        self.exec_path = exec_path
        self.console_exec_path = console_exec_path
        # print(f"{self.exec_path=}")

        self.mh = ModuleHandler()
        check_for_pip()

    def setRm(self, rm):
        self.rm = rm

        if self.std_mode:
            self.out.rm = rm
            self.err.rm = rm

    def loadMeasure(self, rm: RainmeterW = None):
        self.setRm(rm)
        try:
            classPath = rm.RmReadString("Module", "", False)
            print(classPath)

            if classPath != "":
                return self.mh.load_measure(
                    classPath, rm.RmReadString("Loader", "Measure()", False), True
                )
            
            
            infoPath = rm.RmReadPath("Info", "")
            if infoPath != "":
                return self.mh.load_measure(
                    infoPath,
                    rm.RmReadString("Loader", "Measure()", False),
                )
            
            return self.mh.load_measure(
                rm.RmReadPath("Path", "__NONE__"),
                rm.RmReadString("Loader", "Measure()", False),
            )

        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return None

    # Wrappers for measure calls. Used to catch errors and print them to the log.
    def callReload(self, m: MeasureBase, rm, maxValue: float):
        self.setRm(rm)

        # print("RELOAD CALLED")
        try:
            return m.Reload(rm, maxValue)
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

    def callUpdate(self, m: MeasureBase):
        try:
            return m.Update()
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
        return 1.0

    def callGetString(
        self,
        m: MeasureBase,
    ):
        try:
            return m.GetString()
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
        return ""

    def callExecuteBang(self, m: MeasureBase, args):
        try:
            m.ExecuteBang(args)
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

    def callFinalize(self, m: MeasureBase):
        try:
            m.Finalize()
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))

    def callFunc(self, m: MeasureBase, fname: str, args: tuple):
        try:
            # print(args)
            return getattr(m, fname)(*args)
        except Exception as e:
            self.rm.RmLog(self.rm.LOG_ERROR, str(e))
            return None
