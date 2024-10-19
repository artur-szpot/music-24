from enum import Enum
from typing import List, Optional, Dict

from functions.commands.definition.FunctionDefinition import FunctionDefinition
from libs.list_union_util import SimpleList, simple_list
from libs.strings import quoted


def print_flag(value: str) -> str:
    if len(value) == 1:
        return "-" + value
    return "--" + value


def print_flags(values: List[Enum]) -> str:
    return " ".join(print_flag(value.value) for value in values)


def print_command(
    definition: FunctionDefinition,
    args: Optional[List[str]] = None,
    flags: Optional[List[Enum]] = None,
    kwargs: Optional[List[Dict[Enum, SimpleList[str]]]] = None,
):
    parts = [definition.verbs[0]]
    if args:
        parts.extend(quoted(arg) for arg in args)
    if flags:
        parts.append(print_flags(flags))
    if kwargs:
        for kwarg in kwargs:
            for name, values in kwarg.items():
                parts.append(print_flag(name.value))
                parts.extend(quoted(value) for value in simple_list(values))
    return " ".join(parts)
