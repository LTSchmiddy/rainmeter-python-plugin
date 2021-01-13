import sys, json

import measure_host

import PythonLoaderUtils.anon_func as af
from PythonLoaderUtils.rm_stub import RainmeterW
from PythonLoaderUtils.stdhandler import SubInterpStdHandler
from PythonLoaderUtils.load_module_helper import *

parentWrite: SubInterpStdHandler = sys.stdout
parentErr: SubInterpStdHandler = sys.stderr

from PythonLoaderUtils.rm_sp_child import RainmeterSP


def spChildMain():
    print("Starting SP Mainloop")

    # SP STARTUP
    host = measure_host.MeasureHost(False)
    rm_sp = RainmeterSP()

    measureDict = {}

    host.setup(rm_sp, sys.executable)
    while True:
        # try:
        request = json.loads(input())
        if "error" in request:
            print(request)

        if request["type"] == "loadMeasure":
            newMeasure = host.loadMeasure(rm_sp)
            mid = None
            if newMeasure != None:
                mid = id(newMeasure)
            measureDict[mid] = newMeasure
            parentWrite.write(mode="return", content=mid)
            parentWrite.flush()

        elif request["type"] == "callReload":
            measure = measureDict[int(request["mId"])]
            host.callReload(measure, rm_sp, request["maxValue"])
            parentWrite.write(mode="return", content=None)
            parentWrite.flush()

        elif request["type"] == "callUpdate":
            measure = measureDict[int(request["mId"])]
            host.callUpdate(measure)
            parentWrite.write(mode="return", content=host.callUpdate(measure))
            parentWrite.flush()

        elif request["type"] == "callGetString":
            measure = measureDict[int(request["mId"])]
            parentWrite.write(mode="return", content=host.callGetString(measure))
            parentWrite.flush()

        elif request["type"] == "callExecuteBang":
            measure = measureDict[int(request["mId"])]
            host.callExecuteBang(measure)
            parentWrite.write(mode="return", content=None)
            parentWrite.flush()

        elif request["type"] == "callFinalize":
            measure = measureDict[int(request["mId"])]
            host.callFinalize(measure)
            del measureDict[int(request["mId"])]
            parentWrite.write(mode="return", content=None)
            parentWrite.flush()

        elif request["type"] == "callFunc":
            measure = measureDict[int(request["mId"])]
            parentWrite.write(
                mode="return",
                content=host.callFunc(measure, request["fname"], request["args"]),
            )
            parentWrite.flush()

        else:
            print(f"Request Type {request['type']} Unknown!")
            parentWrite.write(mode="return", content=None)
            parentWrite.flush()

        # except Exception as e:
        # print(f"CHILD ERROR: {e}")
        # parentWrite.write(
        #         mode='return',
        #         content=None
        #     )
        # parentWrite.flush()


# Used for testing!!
def spChildMainTEST():
    print("Starting SP Mainloop")

    while True:
        request = input()

        parentWrite.write(
            mode="rm_call",
            content={"func": "RmLog", "args": (4, "RM_CALL WORKS"), "kwargs": {}},
        )

        result = input()
        # print(result)
        parentWrite.write(mode="return", content=result)
