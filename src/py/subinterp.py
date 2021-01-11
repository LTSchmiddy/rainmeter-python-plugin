import sys, os, pathlib, subprocess, pickle, json, time
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Union

import PythonLoaderUtils.anon_func as af
from PythonLoaderUtils.rm_stub import RainmeterW
from PythonLoaderUtils.stdhandler import SubInterpStdHandler
from PythonLoaderUtils.load_module_helper import *

def init():
    print(f"{__file__=}")

class SubInterp:
    # Class variables:
    interp_path: Path = ""
    
    # Instance variables:
    proc: subprocess.Popen
    
    @classmethod
    def get_interp_path(cls) -> Path:
        return cls.interp_path
    
    @classmethod
    def set_interp_path(cls, val: Path):
        cls.interp_path = val
        
    
    def __init__(self, modulePath: Path, execfn: str, log_prefix: str = "_", args: list = [], popen_args: dict={}):
        procArgs = [self.interp_path, __file__, modulePath, execfn, log_prefix] + args
        # procArgs = [self.interp_path,  Path(__file__)]
        print(procArgs)
        self.proc = subprocess.Popen(
            procArgs,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            **popen_args
        )
        
    def exchange(self, rm: RainmeterW, request: dict):        
        requestStr = json.dumps(request) + "\n"
        # print(f"{requestStr}")
        
        self.proc.stdin.write(requestStr.encode('utf8'))
        self.proc.stdin.flush()
        # Request has been made. NOW, we start the exchange loop:
        
        while True:
            if self.proc.poll() is not None:
                print("Python subprocess has ended!")
                raise RuntimeError("Python subprocess has ended!")
            
            raw = self.proc.stdout.readline().decode('utf8').strip()
            
            if len(raw) == 0:
                continue
            
            # print(f"{raw=}")
            try:
                response = json.loads(raw)
            except json.JSONDecodeError as e:
                print(e)
                self.proc.stdin.write(b"ERROR\n")
                self.proc.stdin.flush()
                continue
                
                
            if response['mode'] == 'print':
                # print(f"SP: {response['data']}")
                continue
            
            elif response['mode'] == 'rm_rcall':
                # print(response['data'])
                
                result = getattr(rm, response['data']['func'])(*response['data']['args'], **response['data']['kwargs'])
                self.proc.stdin.write(json.dumps({'result': result}).encode('utf8') + b"\n")
                self.proc.stdin.flush()
                continue
            
            elif response['mode'] == 'rm_call':
                # print(response['data'])
                
                getattr(rm, response['data']['func'])(*response['data']['args'], **response['data']['kwargs'])
                continue
            
            elif response['mode'] == 'return':
                # print(response['data'])
                return response['data']
            
        




def childMain(modulePath: Path, execfn: str, log_prefix: str, *args):
    # time.sleep(10)

    # These classes remember the old TextIO for themselves.
    # No need to store backup references elsewhere.
    sys.stdout = SubInterpStdHandler(sys.stdout, log_prefix + "out.log")
    sys.stderr = SubInterpStdHandler(sys.stderr, log_prefix + "err.log")

    scriptModule = load_module_from_path(modulePath)
    scriptFn = af.rexec(None, f"scriptModule.{execfn}", __locals={"scriptModule": scriptModule })
    return scriptFn(*args)



if __name__ == '__main__':
    # print(sys.argv[1:])
    # time.sleep(10)
    # try:
        childMain(*sys.argv[1:])
    # except Exception as e:
        # print(dir(e))
        # print(e)
        # input("Press enter to close...")