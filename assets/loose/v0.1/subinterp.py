import sys, os, pathlib, subprocess, json, textwrap
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
    handledDeath: bool

    @classmethod
    def get_interp_path(cls) -> Path:
        return cls.interp_path

    @classmethod
    def set_interp_path(cls, val: Path):
        cls.interp_path = val

    def __init__(
        self,
        modulePath: Path,
        execfn: str,
        log_prefix: str = "_",
        args: list = [],
        popen_args: dict = {},
        *,
        use_interp_path=None
    ):
        if use_interp_path is None:
            use_interp_path = self.interp_path
            
        self.handledDeath = False

        # debug_file_path = os.path.join(os.path.dirname(sys.executable), "../debug.txt")
        # use_debug = os.path.isfile(debug_file_path)

        procArgs = [use_interp_path, __file__, modulePath, execfn, log_prefix] + args
        # procArgs = [self.interp_path,  Path(__file__)]
        print(procArgs)
        self.proc = subprocess.Popen(
            procArgs, stdin=PIPE, stdout=PIPE, stderr=PIPE, **popen_args
        )

    def handleSubProcessDeath(self):
        if self.handledDeath:
            return "ERROR: Subprocess dead."

        self.handledDeath = True
        outMessage = self.proc.stdout.read()
        errorMessage = self.proc.stderr.read()
        print(
            textwrap.dedent(
                f"""FATAL ERROR - Python subprocess has died with:
--- out --- :
{outMessage.decode('utf8')}

--- err --- :
{errorMessage.decode('utf8')}

"""
            ).replace("\r", "")
        )
        raise RuntimeError("Python subprocess is dead.")

    def exchange(self, rm: RainmeterW, request: dict):
        if self.proc.poll() is not None:
            return self.handleSubProcessDeath()

        requestStr = json.dumps(request) + "\n"
        # print(f"{requestStr}")

        self.proc.stdin.write(requestStr.encode("utf8"))
        self.proc.stdin.flush()
        # Request has been made. NOW, we start the exchange loop:

        while True:
            if self.proc.poll() is not None:
                return self.handleSubProcessDeath()

            raw = self.proc.stdout.readline().decode("utf8").strip()

            if len(raw) == 0:
                continue

            # print(f"{raw=}")
            try:
                response = json.loads(raw)
            except json.JSONDecodeError as e:
                # print(e)
                print(f"{raw=}")
                # self.proc.stdin.write(
                #     json.dumps({"error": str(e)}).encode("utf8") + b"\n"
                # )
                # self.proc.stdin.flush()
                continue

            if response["mode"] == "print":
                # print(f"SP: {response['data']}")
                continue

            elif response["mode"] == "rm_rcall":
                # print(response['data'])

                result = getattr(rm, response["data"]["func"])(
                    *response["data"]["args"], **response["data"]["kwargs"]
                )
                self.proc.stdin.write(
                    json.dumps({"result": result}).encode("utf8") + b"\n"
                )
                self.proc.stdin.flush()
                continue

            elif response["mode"] == "rm_call":
                # print(response['data'])

                getattr(rm, response["data"]["func"])(
                    *response["data"]["args"], **response["data"]["kwargs"]
                )
                continue

            elif response["mode"] == "return":
                # print(response['data'])
                return response["data"]


def childMain(modulePath: Path, execfn: str, log_prefix: str, *args):
    # to enable the VSCode debugging, create 'debug.txt' in the cwd

    debug_file_path = os.path.join(os.path.dirname(sys.executable), "debug.txt")
    use_debug = os.path.isfile(debug_file_path)
    # if use_debug:

    if use_debug:
        import ptvsd

        port = 3000
        ptvsd.enable_attach(address=("127.0.0.1", port))
        ptvsd.wait_for_attach()

    # These classes remember the old TextIO for themselves.
    # No need to store backup references elsewhere.

    home_dir = pathlib.Path(".")
    log_dir = home_dir.joinpath(".rm_PyPluginSp_logs")

    if not log_dir.exists():
        os.makedirs(log_dir)

    out_log_path = log_dir.joinpath(log_prefix + f"{use_debug=}_out.log")
    err_log_path = log_dir.joinpath(log_prefix + f"{use_debug=}_err.log")

    sys.stdout = SubInterpStdHandler(sys.stdout, str(out_log_path))
    sys.stderr = SubInterpStdHandler(sys.stderr, str(err_log_path))

    # sys.stdout = SubInterpStdHandler(sys.stdout, log_prefix + "out.log")
    # sys.stderr = SubInterpStdHandler(sys.stderr, log_prefix + "err.log")

    print(f"{debug_file_path=}")
    print(f"{use_debug=}")

    scriptModule = load_module_from_path(modulePath)
    print("Module Loading...")
    scriptFn = af.rexec(
        None, f"scriptModule.{execfn}", __locals={"scriptModule": scriptModule}
    )
    print("Module Starting...")
    return scriptFn(*args)


if __name__ == "__main__":
    # print(sys.argv[1:])
    # time.sleep(10)
    # try:
    childMain(*sys.argv[1:])
# except Exception as e:
# print(dir(e))
# print(e)
# input("Press enter to close...")
