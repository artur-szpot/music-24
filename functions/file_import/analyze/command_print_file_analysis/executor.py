from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.file_import.analyze.analyze_files import analyze_files
from functions.file_import.analyze.command_print_file_analysis.flags import (
    PrintFileAnalysisFlags,
    print_file_analysis_flags,
)
from functions.querying.command_list_all_files.executor import (
    list_files_header,
    list_files,
)
from functions.querying.standard_views import ANALYZE_VIEW


def print_file_analysis(args_dict: ArgsDict) -> ExecutionResult:
    show_only_if_error = args_dict.has_flag(
        print_file_analysis_flags[PrintFileAnalysisFlags.ShowOnlyIfError]
    )
    show_only_if_warning = args_dict.has_flag(
        print_file_analysis_flags[PrintFileAnalysisFlags.ShowOnlyIfWarning]
    )
    overwrite_cache = args_dict.has_flag(
        print_file_analysis_flags[PrintFileAnalysisFlags.OverwriteCache]
    )
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
