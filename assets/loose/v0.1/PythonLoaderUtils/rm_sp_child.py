from typing import Any
import sp_child, json

from sp_child import parentWrite


def rm_rcall(func: str, *args, **kwargs) -> Any:
    parentWrite.write(
        mode="rm_rcall", content={"func": func, "args": args, "kwargs": kwargs}
    )
    parentWrite.flush()
    jout = json.loads(input())
    # print(f"{jout=}")
    if "error" in jout:
        raise Exception(f"{jout['error']=}")
    elif "result" in jout:
        return jout["result"]
    else:
        return "ERR"


def rm_call(func: str, *args, **kwargs) -> Any:
    parentWrite.write(
        mode="rm_call", content={"func": func, "args": args, "kwargs": kwargs}
    )
    parentWrite.flush()


class RainmeterSP:
    LOG_ERROR = 1
    LOG_WARNING = 2
    LOG_NOTICE = 3
    LOG_DEBUG = 4

    def __init__(self):
        pass

    def RmReadString(
        self, option: str, default: str, replaceMeasures: bool = False
    ) -> str:
        return rm_rcall("RmReadString", option, default, replaceMeasures)

    def RmReadPath(self, option: str, default: str) -> str:
        return rm_rcall("RmReadPath", option, default)

    def RmReadDouble(self, option: str, default: float) -> float:
        return rm_rcall("RmReadDouble", option, default)

    def RmReadInt(self, option: str, default: int) -> int:
        return rm_rcall("RmReadInt", option, default)

    def RmGetMeasureName(self):
        return rm_rcall("RmGetMeasureName")

    def RmExecute(self, commandStr: str):
        return rm_call("RmExecute", commandStr)

    def RmLog(self, level: int, message: str):
        return rm_call("RmLog", level, message)
