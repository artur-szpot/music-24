import os

from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.execute.ExecutionResult import ExecutionResult
from libs.io import get_all_file_paths


def clear_db_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=clear_db,
        verbs=["clear-database", "clear-db", "cdb"],
        description="Remove all the saved information from the database.",
        category=FunctionCategoryEnum.EditingFiles,
    )


def clear_db(args_dict: ArgsDict) -> ExecutionResult:
    ArgsExtractor.no_args(args_dict)
    all_paths = get_all_file_paths("db/music_files")
    for path in all_paths:
        os.remove(path)
    return ExecutionResult.message(f"Removed {len(all_paths)} files.")
