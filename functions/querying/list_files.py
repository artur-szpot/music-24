from typing import List

from enums.function_categories import FunctionCategoryEnum
from functions.execute.ArgsDict import ArgsDict
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.file_management.MusicFile import MusicFile
from functions.file_management.file_operations import open_file
from functions.help.FunctionHelp import FunctionHelp
from functions.querying.View import standard_view
from libs.io import get_all_files


def list_all_files_help() -> FunctionHelp:
    return FunctionHelp(
        ["list-files", "ls"],
        "Lists all files currently in the database.",
        FunctionCategoryEnum.ViewingFiles,
    )


def list_all_files(args_dict: ArgsDict):
    ArgsExtractor.no_args(args_dict)
    all_paths = get_all_files("db/music_files")
    files = [open_file(path) for path in all_paths]
    return list_files(files)


def list_files(files: List[MusicFile]):
    view = standard_view
    lines: List[str] = [
        view.print_separator_line(),
        view.print_title_line(),
        view.print_separator_line(),
    ]
    index = 1
    for music_file in files:
        music_file.set_view_props(index)
        lines.append(view.print_file(music_file))
        index += 1
    return lines
