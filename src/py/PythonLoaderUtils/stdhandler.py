import sys

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