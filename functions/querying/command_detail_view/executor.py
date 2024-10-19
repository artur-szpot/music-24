from typing import List

from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.file_import.analyze.analyze_files import analyze_file
from functions.lines.Line import Line
from functions.music_file.MusicFile import MusicFile
from functions.querying.command_detail_view.flags import (
    DetailViewFlags,
    detail_view_flags,
)
from functions.querying.file_view_header import file_view_header
from functions.querying.formatting import format_length
from functions.settings.text_color.SchemeColor import SchemeColor


def detail_view(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()
    skip_info = args_dict.has_flag(
        detail_view_flags[DetailViewFlags.ErrorsAndWarningsOnly]
    )
    return ExecutionResult.paginable(
        items=detail_view_exe(file, skip_info), header=[file_view_header(file)]
    )


def check_or_x(value: bool) -> str:
    return "?" if value is None else "✓" if value else "✗"


def detail_view_exe(file: MusicFile, skip_info: bool = False) -> List[Line]:
    details = []
    file = analyze_file(file)
    if not skip_info:
        details.append(Line.key_value("Title", file.title))
        details.append(Line.key_value("Artists", ", ".join(file.artists)))
        details.append(Line.key_value("Length", format_length(file.length).text))
        # soon to be split into groups
        details.append(Line.key_value("Genres", ", ".join(file.genres)))
        details.append(Line.key_value("Rating", (file.rating or 0) / 2))
        details.append(Line.key_value("MLP-related?", check_or_x(file.is_mlp)))
        details.append(Line.key_value("Suitable for Dad?", check_or_x(file.is_dad)))
    for error in file.errors:
        details.append(Line.key_value("Error", error.text, key_color=SchemeColor.BAD))
    for warning in file.warnings:
        details.append(
            Line.key_value("Warning", warning.text, key_color=SchemeColor.WARN)
        )
    if not file.errors and not file.warnings:
        details.append(Line.bold("No errors or warnings", color=SchemeColor.GOOD))
    return details
