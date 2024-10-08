from typing import Dict

from functions.execute.ExecutionResult import ExecutionResult
from functions.music_file.MusicFile import MusicFile

query_cache: Dict[str, ExecutionResult] = {}
file_cache: Dict[str, MusicFile] = {}
