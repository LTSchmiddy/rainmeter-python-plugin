import json, sys
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
    
    def __init__(self, oldStdout: TextIO, logName="subinterp.log"):
        self.oldStdout = oldStdout
        self.logFile = open(logName, 'w')
        self.logName = logName
         
    def write(self, content: str, mode: str = 'print', raw: bool = False):
        if mode == 'print':
            self.logFile.write(content)

        
        out = None
        if raw:
            out = content
        else:
            outDict = {
                'mode': mode,
                'logName': self.logName,
                'data': content
            }
            # Packaging our writes to stdout as json escapes any unwanted newlines and
            # makes it easier the parent process to handle the output.
            
            out = json.dumps(outDict) + "\n"
        self.oldStdout.write(out)
        if mode != 'print' and not self.printOnly:
            self.logFile.write(out)
        
    
    def flush(self):
        self.oldStdout.flush()
        self.logFile.flush()