import os

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.result.ExecutionResult import ExecutionResult
from libs.io import get_all_file_paths


def clear_db_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=clear_db,
        verbs=["clear-database", "clear-db", "cdb"],
        args_validator=ArgsValidator.no_args(),
        description="Remove all the saved information from the database.",
        category=FunctionCategoryEnum.EditingFiles,
    )


def clear_db(args_dict: ArgsDict) -> ExecutionResult:
    all_paths = get_all_file_paths("db/music_files")
    for path in all_paths:
        os.remove(path)
    return ExecutionResult.message(f"Removed {len(all_paths)} files.")
