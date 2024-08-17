from enum import Enum

from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.file_import.analyze_files import analyze_files
from functions.querying.list_files import list_files, list_files_header
from functions.querying.standard_views import ANALYZE_VIEW


class Flags(Enum):
    ShowErrorsOnly = 0


flags = {Flags.ShowErrorsOnly: ["e", "errors-only"]}


def print_file_analysis_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_file_analysis,
        verbs=["analyze-import", "ai"],
        args_validator=ArgsValidator.no_args().flags(flags),
        description="Analyze files from the import directory before importing.",
        category=FunctionCategoryEnum.IngestingFiles,
    )


def print_file_analysis(args_dict: ArgsDict) -> ExecutionResult:
    show_errors_only = args_dict.has_flag(flags[Flags.ShowErrorsOnly])
    return ExecutionResult.table(
        header=list_files_header(ANALYZE_VIEW),
        items=list_files(analyze_files(show_errors_only), ANALYZE_VIEW),
    )
