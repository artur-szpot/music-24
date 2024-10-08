from typing import List, Dict, Any, Optional

from functions.cache.cache import file_cache
from functions.music_file.MusicFile import MusicFile
from functions.file_management.file_operations import open_file


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

    def get_kwarg(self, name: str) -> List[str]:
        return self.kwargs.get(name, [])

    def get_file(self) -> Optional[MusicFile]:
        file = file_cache.get("current_file")
        if file:
            return file
        filename = self.system.get("filename")
        if filename:
            read_file = open_file(filename)
            file_cache["current_file"] = read_file
            return read_file
        return None

    def has_flag(self, flags: List[str]) -> bool:
        return len(list(filter(lambda item: item in self.flags, flags))) > 0
