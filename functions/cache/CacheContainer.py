from typing import Dict, List

from functions.execute.result.ExecutionResult import ExecutionResult
from functions.music_file.MusicFile import MusicFile
from libs.list_union_util import SimpleList


class CacheContainer:
    query_cache: Dict[str, ExecutionResult] = {}
    file_cache: Dict[str, SimpleList[MusicFile]] = {}
    command_stack: List[str] = []
    command_log: List[str] = []
