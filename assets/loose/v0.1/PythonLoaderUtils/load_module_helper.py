from __future__ import annotations
import sys, os, importlib, importlib.util, json, pathlib
from types import ModuleType
from . import anon_func as af
from .json_class import JsonClass
from .module_info import ModuleInfo

platform_extension = af.tget(os.name == "nt", ".pyd", ".so")
module_extensions = (".py", platform_extension)


def module_json_info(path: str):
    minfo = ModuleInfo.load_module_info(path)

    print(minfo.abs_root)
    return minfo.abs_root


def load_module_from_path(scriptPath: str):
    # Handle Module definition via json.
    if scriptPath.endswith("__init__.py"):
        scriptPath = scriptPath.removesuffix("__init__.py")
    elif scriptPath.endswith(".json"):
        scriptPath = module_json_info(scriptPath)

    module_name = os.path.basename(scriptPath).split(".")[0]

    print(f"{module_name=}")
    print(f"{os.path.basename(scriptPath)=}")

    init_path = find_module_init(scriptPath)

    spec = importlib.util.spec_from_file_location(module_name, init_path)
    if spec is None:
        print(
            f"FATAL_ERROR: spec for module {module_name} at '{scriptPath}' could not be created."
        )
        raise ImportError(
            f"FATAL_ERROR: spec for module {module_name} at '{scriptPath}' could not be created."
        )

    # sys.path.append(os.path.dirname(scriptPath))
    # spec.submodule_search_locations.append(os.path.dirname(scriptPath)) ## directory of file)
    # importlib.invalidate_caches()
    loaded = importlib.util.module_from_spec(spec)
    print(spec.submodule_search_locations)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)

    return loaded


def find_module_init(path: str):
    for i in module_extensions:
        if path.endswith(i):
            if os.path.isfile(path):
                print(f"Module root declared: {path}")
                return path
            else:
                raise FileNotFoundError(path)

    init_path = path
    if os.path.isdir(path):
        init_path = os.path.join(path, "__init__").replace("\\", "/")

    for i in module_extensions:
        fullpath = init_path + i
        if os.path.isfile(fullpath):
            print(f"Module root found: {fullpath}")
            return fullpath

    raise FileNotFoundError(path)
