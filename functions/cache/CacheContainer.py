from typing import Dict, Union, List

from functions.execute.ExecutionResult import ExecutionResult
from functions.music_file.MusicFile import MusicFile


class CacheContainer:
    query_cache: Dict[str, ExecutionResult] = {}
    file_cache: Dict[str, Union[MusicFile, List[MusicFile]]] = {}
    command_stack: List[str] = []
