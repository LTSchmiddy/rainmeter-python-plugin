from __future__ import annotations
import sys, os, importlib, importlib.util, pathlib, subprocess
from types import ModuleType
from . import anon_func as af
from .json_class import JsonClass

class ModuleInfo(JsonClass):
    interp_path: str = ""
    
    json_attributes = ("root", "venv", "requirements")
    
    root: str
    venv: str = "venv"
    requirements: str = None

    path: str = None

    @classmethod
    def get_interp_path(cls) -> str:
        return cls.interp_path

    @classmethod
    def set_interp_path(cls, val: str):
        cls.interp_path = val
    
    @classmethod
    def load_module_info(cls, path: str) -> ModuleInfo:
        retVal = cls.new_from_file(path)
        retVal.path = path
        return retVal

    @property
    def dirname(self) -> str:
        return os.path.dirname(self.path)

    @property
    def abs_root(self) -> str:
        return str(pathlib.Path(self.dirname).joinpath(self.root).resolve())

    @property
    def abs_venv(self) -> str:
        return str(pathlib.Path(self.dirname).joinpath(self.venv).resolve())

    @property
    def abs_requirements(self) -> str:
        return str(pathlib.Path(self.dirname).joinpath(self.requirements).resolve())
    
    
    @property
    def abs_venv_pip_exec(self) -> str:
        return str(pathlib.Path(self.abs_venv).joinpath('Scripts').joinpath("pip.exe"))
    
    @property
    def abs_venv_exec(self) -> str:
        return str(pathlib.Path(self.abs_venv).joinpath('Scripts').joinpath("pythonw.exe"))

    @property
    def abs_venv_console_exec(self) -> str:
        return str(pathlib.Path(self.abs_venv).joinpath('Scripts').joinpath("python.exe"))

    def run_setup(self):
        
        if not os.path.isfile(self.abs_requirements):
            return
        
        if os.path.isdir(self.abs_venv):
            return
        
        subprocess.run(
            [
                self.get_interp_path(),
                "-m",
                "virtualenv",
                self.abs_venv
            ]
        )
        
        subprocess.run(
            [
                self.abs_venv_pip_exec,
                "install",
                "-r",
                self.abs_requirements
            ]
        )
        