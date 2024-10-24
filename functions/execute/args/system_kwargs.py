from enum import Enum
from typing import Optional

from libs.list_union_util import SimpleList


class SystemKwargs(Enum):
    Query = 0
    Position = 1
    Filename = 2
    Message = 3
    ErrorMessage = 4

    @staticmethod
    def is_system_kwarg(value: str) -> bool:
        return system_kwargs_reverse(value) is not None


def system_kwargs(value: SystemKwargs) -> SimpleList[str]:
    return {
        SystemKwargs.Query: ["query"],
        SystemKwargs.Position: ["pos"],
        SystemKwargs.Filename: ["filename"],
        SystemKwargs.Message: ["message"],
        SystemKwargs.ErrorMessage: ["error-message"],
    }.get(value, [])


def system_kwargs_reverse(value: str) -> Optional[SystemKwargs]:
    return {
        "query": SystemKwargs.Query,
        "pos": SystemKwargs.Position,
        "filename": SystemKwargs.Filename,
        "message": SystemKwargs.Message,
        "error-message": SystemKwargs.ErrorMessage,
    }.get(value)
