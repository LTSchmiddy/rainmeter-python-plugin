from future import __annotations__

import time

import win32pipe, win32file, pywintypes

def as_pipe_path(name: str) -> str:
    return "\\\\.\\pipe\\{name}"

class PipeConnWrite:
    
    def __init__(self, pipeName: str):
        self.pipeName: str = pipeName
        
        self.pipe = win32pipe.CreateNamedPipe(
            as_pipe_path(self.pipeName),
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        
        win32pipe.ConnectNamedPipe(self.pipe, None)
        
    def send_msg(self, msg: str):
        win32file.WriteFile(self.pipe, str.encode(msg))
        
        
class PipeConnRead():
    def __init__(self, pipeName: str):
        self.pipeName: str = pipeName
        connected = False

        while not connected:
            try:
                self.handle = win32file.CreateFile(
                    r'\\.\pipe\Foo',
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                connected = True
            except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                    
    def read_msg(self) -> str:
        try:
            res = win32pipe.SetNamedPipeHandleState(self.handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                resp = win32file.ReadFile(self.handle, 64*1024).decode()
                print(f"message: {resp}")
        except pywintypes.error as e:
            if e.args[0] == 109:
                print("broken pipe")
                return None