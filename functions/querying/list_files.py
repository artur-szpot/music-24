from typing import List

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.ExecutionResult import ExecutionResult
from functions.file_management.file_operations import open_file
from functions.lines.Line import Line
from functions.music_file.MusicFile import MusicFile
from functions.querying.View import View
from functions.querying.standard_views import STANDARD_VIEW
from libs.io import get_all_files


def list_all_files_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=list_all_files,
        verbs=["list-files", "ls"],
        description="Lists all files currently in the database.",
        category=FunctionCategoryEnum.ViewingFiles,
        following_commands=FunctionFollowingCommands().empty("next-page"),
    )


def list_all_files(args_dict: ArgsDict) -> ExecutionResult:
    all_paths = get_all_files("db/music_files")
    files = [open_file(path) for path in all_paths]
    return ExecutionResult.table(header=list_files_header(), items=list_files(files))


def list_files_header(view: View = None) -> List[Line]:
    view = view or STANDARD_VIEW
    return [
        view.print_separator_line(),
        view.print_title_line(),
        view.print_separator_line(),
    ]


def list_files(files: List[MusicFile], view: View = None) -> List[Line]:
    view = view or STANDARD_VIEW
    lines: List[Line] = []
    for index, music_file in enumerate(files):
        music_file.set_view_props(index)
        lines.append(view.print_file(music_file))
    return lines
