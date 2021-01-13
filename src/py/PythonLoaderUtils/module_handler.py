import os, sys, importlib, importlib.util, pathlib
from types import ModuleType
from . import anon_func as af

from .load_module_helper import load_module_from_path


platform_extension = af.tget(os.name == "nt", ".pyd", ".so")
module_extensions = (".py", platform_extension)


class ModuleHandler:
    modules: dict[str, ModuleType]

    def __init__(self):
        self.modules = {}

    def load_measure(self, scriptPath: str, loader: str, isClassPath: bool = False):
        scriptModule = self.getModule(scriptPath, isClassPath)

        return af.rexec(
            None, f"scriptModule.{loader}", __locals={"scriptModule": scriptModule}
        )
        # return getattr(scriptModule, className)()

    def getModule(self, scriptPath: str, isClassPath: bool = False):
        # print(self.modules)

        if not isClassPath:
            scriptPath = str(pathlib.Path(scriptPath).resolve())

        if scriptPath in self.modules.keys():
            return self.modules[scriptPath]
        else:
            return self.loadNewModule(scriptPath, isClassPath)

    def loadNewModule(self, scriptPath: str, isClassPath: bool = False) -> ModuleType:
        loaded = None

        if isClassPath:
            loaded = importlib.import_module(scriptPath)
        else:
            loaded = load_module_from_path(scriptPath)
        self.modules[scriptPath] = loaded
        # sys.path.pop()

        return loaded
