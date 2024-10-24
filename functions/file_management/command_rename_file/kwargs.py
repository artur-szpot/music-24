from enum import Enum

from libs.list_union_util import SimpleList


class RenameFileKwargs(Enum):
    NewName = 0


def rename_file_kwargs(value: RenameFileKwargs) -> SimpleList[str]:
    return {RenameFileKwargs.NewName: ["new-name", "new", "to"]}.get(value, [])
