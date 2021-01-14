import os
from types import FunctionType
from typing import Union

from colors import color


def mkdir_if_missing(dir_path: str):
    if not os.path.isdir(dir_path):
        # os.mkdir(dir_path)
        os.makedirs(dir_path)


def list_contains(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return True
    return False


def list_get(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return x
    return None


def get_dir_tree(
    current_dir,
    callback: FunctionType = None,
    to_ignore: Union[tuple, list] = ("__pycache__",),
):
    dir_cont = os.listdir(current_dir)

    dir_dict = {"path": current_dir, "dirs": {}, "files": {}}

    for i in dir_cont:
        if i in to_ignore:
            continue

        fullpath = os.path.join(current_dir, i).replace("\\", "/")

        additional_info = {}
        if callback is not None:
            shouldSkip = callback(i, fullpath, current_dir, additional_info)

            # I should probably re-write this line:
            # if not (shouldSkip is None or bool(shouldSkip) is True):
            if shouldSkip:
                print(f"Skipping {fullpath}")
                continue

        if os.path.isfile(fullpath):
            additional_info.update({"path:": fullpath})
            dir_dict["files"][i] = additional_info

        elif os.path.isdir(fullpath):
            additional_info.update(get_dir_tree(fullpath, callback, to_ignore))
            dir_dict["dirs"][i] = additional_info

    return dir_dict


def print_color(fg: str, *args, **kwargs):
    p_list = []
    for i in args:
        p_list.append(color(str(i), fg=fg))

    print(*p_list, **kwargs)


def print_error(*args, **kwargs):
    print_color("red", *args, **kwargs)


def print_warning(*args, **kwargs):
    print_color("yellow", *args, **kwargs)


def yn_prompt(msg: str = "", default=None):
    while True:
        result = input(msg).lower()

        if result == "y":
            return True
        if result == "n":
            return False

        if default is not None:
            print_error("Using default...")
            return default

        print_error("Invalid response. Try again...")


def exec_path(path: str):
    if os.name == "nt":
        return path + ".exe"
    return path
