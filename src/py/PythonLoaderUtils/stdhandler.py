import json, sys
from threading import main_thread
import threading
from typing import TextIO
import PythonLoaderUtils.anon_func as af


class StdHandler:
    def __init__(self, fname: str, rm, mode):
        self.fname = fname
        self.rm = rm
        self.mode = mode

    def write(self, s: str):
        to_write = s.strip()
        if to_write != "":
            self.rm.RmLog(self.mode, f"{self.fname}: {s}")

    def flush(self):
        pass


sys.stdout


class SubInterpStdHandler:
    oldStdout: TextIO
    logName: str
    logFile: TextIO

    printOnly = True

    @classmethod
    def load_imports(cls):
        import threading, multiprocessing

        cls._threading = threading
        cls._multiprocessing = multiprocessing

    def __init__(self, oldStdout: TextIO, logName="subinterp.log"):
        self.oldStdout = oldStdout
        self.logFile = open(logName, "w")
        self.logName = logName

        self.load_imports()

    def write(self, content: str, mode: str = "print", raw: bool = False):
        if mode != "print":
            if self._threading.current_thread() != self._threading.main_thread():
                raise self._threading.ThreadError(
                    "Non-print write modes can pnly be used from the main thread."
                )
            elif (
                type(self._multiprocessing.current_process())
                == self._multiprocessing.Process
            ):
                raise self._multiprocessing.ProcessError(
                    "Non-print write modes can pnly be used from the main process."
                )

        else:
            self.logFile.write(content)

        out = None
        if raw:
            out = content
        else:
            outDict = {"mode": mode, "logName": self.logName, "data": content}
            # Packaging our writes to stdout as json escapes any unwanted newlines and
            # makes it easier the parent process to handle the output.

            out = json.dumps(outDict) + "\n"
        self.oldStdout.write(out)
        if mode != "print" and not self.printOnly:
            self.logFile.write(out)

    def flush(self):
        self.oldStdout.flush()
        self.logFile.flush()

    def close(self):
        self.oldStdout.close()
        self.logFile.close()