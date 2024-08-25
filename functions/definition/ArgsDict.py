from typing import List, Dict, Any, Optional

from functions.file_management.MusicFile import MusicFile
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
        return self.args[index]

    def get_kwarg(self, name: str) -> List[str]:
        return self.kwargs.get(name, [])

    def get_file(self) -> Optional[MusicFile]:
        file = self.system.get("file")
        if file:
            return file
        filename = self.system.get("filename")
        if filename:
            return open_file(filename)
        return None

    def has_flag(self, flags: List[str]) -> bool:
        return len(list(filter(lambda item: item in self.flags, flags))) > 0
