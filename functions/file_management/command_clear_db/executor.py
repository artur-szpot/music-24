import os

from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from libs.io import get_all_file_paths


def clear_db(args_dict: ArgsDict) -> ExecutionResult:
    all_paths = get_all_file_paths("db/music_files")
    for path in all_paths:
        os.remove(path)
    return ExecutionResult.message(f"Removed {len(all_paths)} files.")
