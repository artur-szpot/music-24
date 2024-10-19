from enum import Enum
from typing import List, Dict, Any, Optional

from functions.cache import cache
from functions.file_management.file_operations import open_file
from functions.music_file.MusicFile import MusicFile


class ArgsDict:
    def __init__(
        self,
        args: List[str],
        kwargs: Dict[str, List[str]],
        flags: List[str],
        system: Dict[str, Any] = None,
    ):
        self.args = args
        self.kwargs = kwargs
        self.flags = flags
        self.system = system or {}

    def get_arg(self, index: int = 0) -> Optional[str]:
        try:
            return self.args[index]
        except:
            return None

    def get_numeric_arg(self, index: int = 0) -> Optional[int]:
        try:
            return int(self.args[index])
        except:
            return None

    def get_kwarg(self, name: Enum) -> List[str]:
        return self.kwargs.get(name.value, [])

    def get_file(self) -> Optional[MusicFile]:
        file = cache.get_current_file()
        if file:
            return file
        filename = self.system.get("filename")
        if filename:
            read_file = open_file(filename)
            cache.set_current_file(read_file)
            return read_file
        return None

    def has_flag(self, flags: List[str]) -> bool:
        return (
            len(
                list(
                    filter(
                        lambda item: item in self.flags,
                        [flag for flag in flags],
                    )
                )
            )
            > 0
        )
