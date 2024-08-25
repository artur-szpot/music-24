from enum import Enum
from typing import List

from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.Line import Line, TextColor
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.ArgsValidator import ArgsValidator
from functions.file_management.MusicFile import MusicFile
from functions.file_management.file_operations import open_file
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
        args_validator=ArgsValidator.file_and_no_args().flags(flags)
    )


def detail_view(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()
    skip_info = args_dict.has_flag(flags[Flags.ErrorsAndWarningsOnly])
    return ExecutionResult.paginable(items=detail_view_exe(file, skip_info))


def check_or_x(value:bool)->str:
    return  '✓' if value else '✗'


def detail_view_exe(file: MusicFile,skip_info:bool=False)->List[Line]:
    details = []
    filename = file.path.split('\\')[-1]
    details.append(Line.key_value("File name",filename))
    if not skip_info:
        details.append(Line.key_value("Title",file.title))
        details.append(Line.key_value("Authors", ', '.join(file.authors)))
        details.append(Line.key_value("Length",format_length(file.length).text))
        # soon to be split into groups
        details.append(Line.key_value("Genres",', '.join(file.genres)))
        details.append(Line.key_value("Rating", file.rating/2))
        details.append(Line.key_value("MLP-related?",check_or_x(file.is_mlp)))
        details.append(Line.key_value("Suitable for Dad?",check_or_x(file.is_dad)))
    if file.errors:
        details.append(Line.bold("Errors:",color=TextColor.RED))
        for error in file.errors:
            details.append(Line.simple(f" • {error}"))
    if file.warnings:
        details.append(Line.bold("Warnings:",color=TextColor.LIGHT_RED))
        for warning in file.warnings:
            details.append(Line.simple( f" • {warning}"))
    return details
