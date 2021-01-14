import sys, os, subprocess, pathlib
from .module_info import ModuleInfo

interp_path: str = None

# Thiss module is only useful on the embedded side.
scriptsFolder = pathlib.Path(os.path.dirname(sys.executable)).joinpath("PythonLoaderScripts")

def check_for_pip() -> bool:
    try:
        import pip

        print("Pip Found!")
        return True
    except ImportError as e:
        print("Pip Not Found!")
        return False


def install_pip() -> bool:
    global interp_path, scriptsFolder

    pip_run_args = [
        interp_path,
        str(scriptsFolder.joinpath("install_pip.py")),
        sys.executable
    ]
    print(f"{pip_run_args=}")
    install_script = subprocess.Popen(pip_run_args)
    install_script.wait()
    
    print(f"{install_script.returncode=}")
    sys.exit()


def setup_minfo(minfo: ModuleInfo):
    setup_run_args = [
        interp_path,
        str(scriptsFolder.joinpath("module_info_setup.py")),
        minfo.path
    ]
    
    print(f"{setup_run_args=}")
    install_script = subprocess.Popen(setup_run_args)
    install_script.wait()
    
    print(f"{install_script.returncode=}")
