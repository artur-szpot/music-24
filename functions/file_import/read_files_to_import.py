from typing import List

from functions.file_import.read_file import read_file
from functions.music_file.MusicFile import MusicFile
from libs.io import get_all_file_paths


def read_files_to_import() -> List[MusicFile]:
    all_paths = get_all_file_paths("import")
    return [read_file(path) for path in all_paths]
