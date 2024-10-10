from enum import Enum

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.file_import.analyze_files import analyze_files
from functions.querying.list_files import list_files, list_files_header
from functions.querying.standard_views import ANALYZE_VIEW


class Flags(Enum):
    ShowOnlyIfError = 0
    ShowOnlyIfWarning = 1
    OverwriteCache = 2


flags = {
    Flags.ShowOnlyIfError: ["e", "errors"],
    Flags.ShowOnlyIfWarning: ["w", "warnings"],
    Flags.OverwriteCache: ["o", "overwrite"],
}


def print_file_analysis_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_file_analysis,
        verbs=["analyze-import", "ai"],
        args_validator=ArgsValidator.no_args().flags(flags),
        description="Analyze files from the import directory before importing.",
        category=FunctionCategoryEnum.IngestingFiles,
        following_commands=FunctionFollowingCommands().empty("next-page"),
    )


def print_file_analysis(args_dict: ArgsDict) -> ExecutionResult:
    show_only_if_error = args_dict.has_flag(flags[Flags.ShowOnlyIfError])
    show_only_if_warning = args_dict.has_flag(flags[Flags.ShowOnlyIfWarning])
    overwrite_cache = args_dict.has_flag(flags[Flags.OverwriteCache])
    files = analyze_files(
        show_only_if_error=show_only_if_error,
        show_only_if_warning=show_only_if_warning,
        overwrite_cache=overwrite_cache,
    )
    return ExecutionResult.table(
        header=list_files_header(ANALYZE_VIEW),
        items=list_files(files, ANALYZE_VIEW),
        files=files,
    )
