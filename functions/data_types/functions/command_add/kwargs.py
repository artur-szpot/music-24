from enum import Enum

from libs.list_union_util import SimpleList


class AddKwargs(Enum):
    Aliases = 0
    Misspellings = 1
    Category = 2


def add_kwargs(value: AddKwargs) -> SimpleList[str]:
    return {
        AddKwargs.Aliases: ["aliases", "alias", "a"],
        AddKwargs.Misspellings: ["misspellings", "miss", "m"],
        AddKwargs.Category: ["category", "cat", "c"],
    }.get(value, [])
