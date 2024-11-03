from enum import Enum
from typing import List, Optional, Dict, Callable

from libs.list_union_util import SimpleList, simple_list
from libs.strings import quoted


def print_flag(
    name: Enum, translation_function: Callable[[Enum], SimpleList[str]]
) -> str:
    value = simple_list(translation_function(name))
    if value is None or not len(value):
        raise KeyError(
            f"Translation for {name} not found in supplied translation dictionary"
        )
    value = value[0]
    if len(value) == 1:
        return "-" + value
    return "--" + value


def print_flags(
    values: List[Enum], translation_function: Callable[[Enum], SimpleList[str]]
) -> str:
    return " ".join(print_flag(value, translation_function) for value in values)


def print_command(
    verbs: List[str],
    args: Optional[List[str]] = None,
    flags: Optional[List[Enum]] = None,
    flag_dict: Callable[[any], SimpleList[str]] = None,
    kwargs: Optional[List[Dict[Enum, SimpleList[str]]]] = None,
    kwarg_dict: Callable[[any], SimpleList[str]] = None,
):
    parts = [verbs[0]]
    if args:
        parts.extend(quoted(arg) for arg in args)
    if flags:
        if not flag_dict:
            raise ValueError("Flags supplied without supporting translation dictionary")
        parts.append(print_flags(flags, flag_dict or {}))
    if kwargs:
        if not kwarg_dict:
            raise ValueError(
                "Kwargs supplied without supporting translation dictionary"
            )
        for kwarg in kwargs:
            for name, values in kwarg.items():
                parts.append(print_flag(name, kwarg_dict or {}))
                parts.extend(quoted(value) for value in simple_list(values))
    return " ".join(parts)
