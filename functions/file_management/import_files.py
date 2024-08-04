from typing import List

from mutagen import File

from enums.function_categories import FunctionCategoryEnum
from functions.execute.ArgsDict import ArgsDict
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.file_management.MusicFile import MusicFile
from functions.file_management.RatingMapper import RatingMapper
from functions.file_management.file_operations import save_new_file
from functions.help.FunctionHelp import FunctionHelp
from functions.querying.list_files import list_files
from libs.io import get_all_file_paths, create_directory


def read_file(path: str) -> MusicFile:
    mutagen_file = File(path)
    music_file = MusicFile(
        {
            "authors": [str(author) for author in mutagen_file.tags.get("TPE1")],
            "genres": [str(author) for author in mutagen_file.tags.get("TCON")],
            "title": str(mutagen_file.tags.get("TIT2")),
            "path": path,
            "length": int(mutagen_file.info.length),
            "rating": RatingMapper.from_mp3_tags(
                int(mutagen_file.tags["POPM:no@email"].rating)
            ),
            "is_mlp": bool(mutagen_file.tags["COMM:Songs-DB_Custom3:XXX"]),
            "is_dad": bool(mutagen_file.tags["COMM:Songs-DB_Custom2:XXX"]),
            "is_ready": bool(mutagen_file.tags["COMM:Songs-DB_Custom1:XXX"]),
        }
    )
    return music_file


def read_files() -> List[MusicFile]:
    all_paths = get_all_file_paths("import")
    return [read_file(path) for path in all_paths]


def analyze_files() -> List[MusicFile]:
    files = read_files()
    for file in files:
        errors = []
        if not len(file.authors):
            errors.append("No authors in tags")
        for author in file.authors:
            if "," in author:
                errors.append(f"Author with illegal symbols in their name: {author}")
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
    return files


def print_file_analysis_help() -> FunctionHelp:
    return FunctionHelp(
        ["analyze-import", "ai"],
        "Analyze files from the import directory before importing.",
        FunctionCategoryEnum.IngestingFiles,
    )


def print_file_analysis(args_dict: ArgsDict) -> List[str]:
    ArgsExtractor.no_args(args_dict)
    return list_files(analyze_files())


def import_files_help() -> FunctionHelp:
    return FunctionHelp(
        ["import-files", "if"],
        "Import all files from the import directory.",
        FunctionCategoryEnum.IngestingFiles,
    )


def import_files(args_dict: ArgsDict) -> List[str]:
    ArgsExtractor.no_args(args_dict)
    files = read_files()
    # move files
    # NOW create file_management files
    create_db_files(files)
    return [f"Successfully imported {len(files)} files"]
    # return [f'added files: {len(files)}']


def create_db_files(music_files: List[MusicFile]) -> None:
    create_directory("file_management")
    for music_file in music_files:
        save_new_file(music_file)
