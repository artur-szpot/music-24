from typing import List

from functions.file_import.read_files_to_import import read_files_to_import
from functions.file_management.MusicFile import MusicFile


def analyze_files(show_if_error: bool = False, show_if_warning: bool = False) -> List[MusicFile]:
    files = read_files_to_import()
    files_to_show = []
    for file in files:
        if not file.errors:
            errors = []
            warnings = []
            if not len(file.authors):
                errors.append("No authors in tags")
            for author in file.authors:
                if "," in author:
                    errors.append(
                        f"Author with illegal symbols in their name: {author}"
                    )
            if not len(file.genres):
                errors.append("No genres in tags")
            for genre in file.genres:
                if "," in genre:
                    errors.append(f"Genre with illegal symbols in their name: {genre}")
            if not len(file.title):
                errors.append("No title set")
            if file.rating is None or file.rating < 0 or file.rating > 10:
                errors.append(f"Invalid file rating: {file.rating}")
            if file.is_dad is None:
                errors.append(f"Dad flag not set")
            if file.is_mlp is None:
                errors.append(f"MLP flag not set")
            if file.is_ready is None:
                errors.append(f"Ready flag not set")
            file.errors = errors
            file.warnings = warnings
        if not (show_if_error or show_if_warning) or (show_if_error and len(file.errors)) or (show_if_warning and len(file.warnings)):
            files_to_show.append(file)
    return files_to_show
