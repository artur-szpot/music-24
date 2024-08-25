import json
from typing import List

from functions.file_management.MusicFile import MusicFile
from libs.io import get_all_files


def open_file(filename: str) -> MusicFile:
    with open(f"db/music_files/{filename}", mode="r") as current_file:
        file_content = json.loads(current_file.read())
    return MusicFile(file_content)


def save_file(filename: str, music_file: MusicFile) -> None:
    with open(f"db/music_files/{filename}.json", mode="w") as current_file:
        current_file.write(json.dumps(music_file.to_dict()))


def save_new_file(music_file: MusicFile) -> None:
    filename = f"{get_new_id()}.json"
    with open(f"db/music_files/{filename}", mode="w") as current_file:
        music_file.filename = filename
        current_file.write(json.dumps(music_file.to_dict()))


def get_new_id() -> int:
    all_paths = [
        int(filename.split(".")[0]) for filename in get_all_files("db/music_files")
    ]
    if not all_paths:
        return 0
    return max(all_paths) + 1


def create_db_files(music_files: List[MusicFile]) -> None:
    for music_file in music_files:
        save_new_file(music_file)
