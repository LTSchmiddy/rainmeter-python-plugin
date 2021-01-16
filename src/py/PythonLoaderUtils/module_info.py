from __future__ import annotations
import sys, os, importlib, importlib.util, pathlib, subprocess
from types import ModuleType
from . import anon_func as af
from .json_class import JsonClass

class ModuleInfo(JsonClass):
    interp_path: str = ""
    
    json_attributes = (
        "root",
        "venv", 
        "requirements", 
        "working_directory",
        "allow_globals",
        "overinstall_globals",
        "update_venv",
        "siKey",
    )
    
    root: str
    venv: str = "venv"
    requirements: str = None
    working_directory: str = "./"
    allow_globals: bool = True
    overinstall_globals: bool = True
    update_venv: bool = False
    # Not yet implemented:
    siKey: str = None

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

    def save_module_info(self, path: str = None):
        if path is None:
            path = self.path
            
        self.save_json_file(path)
    
    @property
    def active_siKey(self) -> str:
        if self.siKey is None:
            return self.path
        return self.siKey
    
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
    
    @property
    def abs_working_directory(self) -> str:
        return str(pathlib.Path(self.dirname).joinpath(self.working_directory).resolve())

    
    @property
    def should_setup_run(self):
        if not os.path.isfile(self.abs_requirements):
            return False

        if not os.path.isdir(self.abs_venv):
            return True
        
        if self.update_venv:
            return True
        
        return False
    
    def setup_dependencies(self):
        if not os.path.isfile(self.abs_requirements):
            return
        
        if not os.path.isdir(self.abs_venv):
            venv_args = [
                self.get_interp_path(),
                "-m",
                "virtualenv",
                self.abs_venv
            ]
            
            if self.allow_globals:
                venv_args += ["--system-site-packages"]
            
            # print(f"{venv_args=}")
            
            init_proc = subprocess.run(
                venv_args
            )
            

            # print(f"{init_proc=}")

            self.update_venv = True
        else:
            print(f"VENV FOUND @ {self.abs_venv}")
        
        
        if self.update_venv:
            pip_args = [
                self.abs_venv_pip_exec,
                "install",
                "-r",
                self.abs_requirements
            ]
            
            if self.overinstall_globals:
                pip_args += ["--ignore-installed"]
        
            subprocess.run(
                pip_args
            )
            
        self.update_venv = False
        self.save_module_info()
        