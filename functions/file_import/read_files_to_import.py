from typing import List

from functions.cache import cache
from functions.file_import.read_file import read_file
from functions.music_file.MusicFile import MusicFile
from libs.io import get_all_file_paths


def read_files_to_import(overwrite_cache: bool = False) -> List[MusicFile]:
    if not overwrite_cache:
        cached = cache.get_files_to_import()
        if cached is not None:
            return cached
    all_paths = get_all_file_paths("import")
    read = [read_file(path) for path in all_paths]
    cache.set_files_to_import(read)
    return read
