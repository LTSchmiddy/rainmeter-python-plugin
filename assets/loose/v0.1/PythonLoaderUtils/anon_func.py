"""
Python Anonymous Functions Library
Created by LT_Schmiddy (Alex Schmid) on 9/25/2020
"""

import inspect
import textwrap
from types import CodeType, FunctionType

# code_class = type(compile("", "<string>", 'exec'))
from typing import Any, Union


def _get_exec_name(
    frame_info: inspect.FrameInfo, prefix: str = "anon_func.rexec"
) -> str:
    return (
        f"<{prefix} (execution) @ function `{frame_info.function}`,"
        f" file '{frame_info.filename}', line {frame_info.lineno}>"
    )


def _get_r_eval_name(
    frame_info: inspect.FrameInfo, prefix: str = "anon_func.rexec"
) -> str:
    return (
        f"<{prefix} (return evaluation) @ function `{frame_info.function}`,"
        f" file '{frame_info.filename}', line {frame_info.lineno}>"
    )


def rexec(
    p_code: Union[str, CodeType, None] = None,
    p_return: Union[str, CodeType, None] = None,
    __globals: Union[dict, None] = None,
    __locals: Union[dict, None] = None,
    __prefix: str = "anon_func.rexec",
    __dedent: bool = True,
) -> Any:
    """
    Indented to work like the `exec()` builtin, but able to return a value.
    Accepts strings or code objects like those returned from `compile()`.
    By default, it uses the globals and locals from the calling stack-frame.
    Useful for squeezing extra statements into a lambda function.

    Since return statements in `exec()` do not recognize when they are inside a function,
    this is not a viable method for returning a value. Instead, after the exec code finishes
    running, `eval(p_return)` is used on the same namespace to get a value to return.

    `p_code` and `p_return` are both allowed to be blank or None. If p_code is blank, it is simply
    ignored and only `p_return` is evaluated. If `p_return` is blank, None is returned.

    The `prefix` parameter is fed into the beginning of the `filename` parameter of the `compile()`
    builtin, and is very useful for debugging and picking through traceback messages.

    The parameters `__globals` and `__locals` allow you to specify dicts of globals and locals
    to use instead of the default (Similar to the `__globals` and `__locals` parameter in `exec()`).

    :param p_code: The code to execute.
    :param p_return: An evaluation to run, the result of which will be returned.
    :param __prefix: A prefix for the filename string of the code you're running.
    :param __globals: Manually specify global variables to use.
    :param __locals: Manually specify local variables to use.
    :param __dedent: If p_code is a string, should it be de-indented before execution?
    :return: The returned value from `p_return`.
    """
    # Gets the frame for the function call.
    # Since this code is inside a function, `frames` will always have at least 2 members.
    frame_info = inspect.stack()[1]

    if __globals is None:
        __globals = frame_info.frame.f_globals
    if __locals is None:
        __locals = frame_info.frame.f_locals

    # print(f"{use_locals}")
    # Handle function execution:

    if p_code is not None:
        # Did the execution code come pre-compiled?
        if isinstance(p_code, CodeType):
            exec(p_code, __globals, __locals)
        # Did we get a source code string?
        elif isinstance(p_code, str) and p_code.strip() != "":
            if __dedent:
                p_code = textwrap.dedent(p_code)

            exec(
                compile(p_code, _get_exec_name(frame_info, __prefix), "exec"),
                __globals,
                __locals,
            )

    # Are we supposed to try to return something?
    if p_return is None:
        return None

    # Generate return evaluation filename string:

    # Did the return code come pre-compiled?
    if isinstance(p_return, CodeType):
        return eval(p_return, frame_info.frame.f_globals, frame_info.frame.f_locals)
    # Did we get a source code string?
    elif isinstance(p_return, str) and p_return.strip() != "":
        return eval(
            compile(p_return, _get_r_eval_name(frame_info, __prefix), "eval"),
            __globals,
            __locals,
        )

    return None


def tget(
    p_expression: Any, r_true=None, r_false=None, do_conversion: bool = True
) -> Any:
    """
    Designed to function like the ternary operator (`?`) in c-based languages.
    For best results, you can simply enter an expression that evaluates to a boolean
    (such as `x==5`) or another type that can be converted to a boolean with bool(`bool`).
    By default, this type conversion is done automatically, to replicate the concept of 'truthiness'
    in `if` statements.

    Unlike some other methods in this module, passing a string into `p_expression` will not evaluate it as code.
    Enter your evaluation as Python code directly. Technically, the expression will be processed before
    it's passed to this function.

    Really, this function just serves as a wrapper for `(if_false, if_true)[condition]`

    :param p_expression: The condition to evaluated.
    :param r_true: Return this if true.
    :param r_false: Return this if false.
    :param do_conversion: Use 'truthiness'?
    :return:
    """
    if do_conversion:
        p_expression = bool(p_expression)
    return (r_false, r_true)[p_expression]


# Anonymous generation of regular functions:
def func(
    f_args: Union[str, tuple, list, None] = None,
    f_code: str = "pass",
    collect_locals: bool = True,
    name: str = "anonymous_function",
    __prefix: str = "anon_func.func",
    __reindent_size: int = 4,
    __globals: Union[dict, None] = None,
    __locals: Union[dict, None] = None,
    __print_func_code: bool = False,
    __return_func_code: bool = False,
) -> Union[FunctionType, str]:
    """
    The moment you've all been waiting for. This method will create anonymous functions for you.


    :param f_args:
    :param f_code:
    :param collect_locals:
    :param name:
    :param __prefix:
    :param __reindent_size:
    :param __globals:
    :param __locals:
    :param __print_func_code:
    :param __return_func_code:
    :return: Your new, anonymous function.
    """
    if collect_locals:
        if isinstance(f_args, str) and f_args.strip() != "":
            f_args += ", __update_locals, __secret_frame,"

        elif (isinstance(f_args, tuple) or isinstance(f_args, list)) and len(
            f_args
        ) > 0:
            f_args = ", ".join(f_args) + ", __update_locals, __secret_frame"
        else:
            f_args = "__update_locals, __secret_frame"
    elif isinstance(f_args, tuple) or isinstance(f_args, list):
        if len(f_args) > 0:
            f_args = ", ".join(f_args)
        else:
            f_args = ""

    if f_code is None or f_code == "":
        f_code = "pass"

    # Gets the frame for the function call.
    # Since this code is inside a function, `frames` will always have at least 2 members.
    frame_info = inspect.stack()[1]
    # __locals_frame = frame_info.frame

    if __globals is None:
        __globals = frame_info.frame.f_globals
    if __locals is None:
        __locals = frame_info.frame.f_locals

    func_text = f"def {name}({f_args}):\n"
    secret_frame = None
    if collect_locals:
        secret_frame = inspect.stack()[1].frame
        func_text += f"{(' ' * __reindent_size)}if __update_locals is not None:\n"
        # func_text += f"{(' ' * __reindent_size * 2)}__secret_locals.update(__update_locals)\n"
        func_text += f"{(' ' * __reindent_size * 2)}__secret_frame.f_locals.update(__update_locals)\n"
        for i in secret_frame.f_locals.keys():
            func_text += (
                f"{(' ' * __reindent_size)}{i} = __secret_frame.f_locals['{i}']\n"
            )

    func_text += _adjust_func_string_indentation(f_code, __reindent_size)
    if __print_func_code:
        print(str() + func_text)
    if __return_func_code:
        return func_text

    out_func: FunctionType = rexec(
        func_text,
        name,
        __prefix=f"{name} from {__prefix}",
        __globals=__globals,
        # We don't ACTUALLY want this function added to the local namespace, so we'll make a duplicate.
        # As long as we feed rexec the original global dict, this shouldn't cause any problems.
        __locals=__locals.copy(),
    )

    if collect_locals:
        if out_func.__defaults__ is not None:
            out_func.__defaults__ += (
                None,
                secret_frame,
            )
        else:
            out_func.__defaults__ = (
                None,
                secret_frame,
            )

    return out_func


def _adjust_func_string_indentation(code_str: str, reindent_size: int = 4) -> str:
    """
    This function handles the actual re-indenting of the function codde from `func()`
    :param code_str: The code to re-indent.
    :param reindent_size: Number of spaces to indent each nested block. The standard in Python is 4 spaces.
    :return: The re-indented code.
    """

    return textwrap.indent(
        textwrap.dedent(code_str),
        " " * reindent_size,
        lambda line: line.strip != "",
    )


__all__ = ("rexec", "tget", "func")
