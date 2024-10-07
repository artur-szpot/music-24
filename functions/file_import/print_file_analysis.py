from enum import Enum

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.file_import.analyze_files import analyze_files
from functions.querying.list_files import list_files, list_files_header
from functions.querying.standard_views import ANALYZE_VIEW


class Flags(Enum):
    ShowIfError = 0
    ShowIfWarning = 1


flags = {Flags.ShowIfError: ["e", "errors"], Flags.ShowIfWarning: ["w", "warnings"]}


def print_file_analysis_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_file_analysis,
        verbs=["analyze-import", "ai"],
        args_validator=ArgsValidator.no_args().flags(flags),
        description="Analyze files from the import directory before importing.",
        category=FunctionCategoryEnum.IngestingFiles,
        default_command="next-page",
    )


def print_file_analysis(args_dict: ArgsDict) -> ExecutionResult:
    show_if_error = args_dict.has_flag(flags[Flags.ShowIfError])
    show_if_warning = args_dict.has_flag(flags[Flags.ShowIfWarning])
    files = analyze_files(show_if_error=show_if_error, show_if_warning=show_if_warning)
    return ExecutionResult.table(
        header=list_files_header(ANALYZE_VIEW),
        items=list_files(files, ANALYZE_VIEW),
        files=files,
    )
