from enum import Enum
from typing import List

from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.file_management.MusicFile import MusicFile
from functions.lines.Line import Line
from functions.lines.LineElement import LineElement
from functions.lines.LineList import LineList
from functions.lines.SchemeColor import SchemeColor
from functions.querying.formatting import format_length


class Flags(Enum):
    ErrorsAndWarningsOnly = 0


flags = {Flags.ErrorsAndWarningsOnly: ["e", "w"]}


def print_detail_view_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=detail_view,
        verbs=["detail-view", "d"],
        description="Lists details of the chosen file.",
        category=FunctionCategoryEnum.ViewingFiles,
        args_validator=ArgsValidator.file_and_no_args().flags(flags),
    )


def detail_view(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()
    skip_info = args_dict.has_flag(flags[Flags.ErrorsAndWarningsOnly])
    return ExecutionResult.paginable(
        items=detail_view_exe(file, skip_info), header=[detail_view_header(file)]
    )


def check_or_x(value: bool) -> str:
    return "?" if value is None else "✓" if value else "✗"


def detail_view_header(file: MusicFile) -> Line:
    return Line.key_value("File name", file.filename)


def detail_view_exe(file: MusicFile, skip_info: bool = False) -> List[Line]:
    details = []
    if not skip_info:
        details.append(Line.key_value("Title", file.title))
        details.append(Line.key_value("Authors", ", ".join(file.authors)))
        details.append(Line.key_value("Length", format_length(file.length).text))
        # soon to be split into groups
        details.append(Line.key_value("Genres", ", ".join(file.genres)))
        details.append(Line.key_value("Rating", file.rating / 2))
        details.append(Line.key_value("MLP-related?", check_or_x(file.is_mlp)))
        details.append(Line.key_value("Suitable for Dad?", check_or_x(file.is_dad)))
    if file.errors:
        header = LineElement.bold("Errors:", color=SchemeColor.BAD)
        details.extend(
            LineList.list([Line.simple(error) for error in file.errors], header)
        )
    if file.warnings:
        header = LineElement.bold("Warnings:", color=SchemeColor.BAD)
        details.extend(
            LineList.list([Line.simple(warning) for warning in file.warnings], header)
        )
    if not file.errors and not file.warnings:
        details.append(Line.bold("No errors or warnings", color=SchemeColor.GOOD))
    return details
