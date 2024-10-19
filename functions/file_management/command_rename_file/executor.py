import os

from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.file_import.analyze.analyze_files import analyze_file
from functions.file_management.command_rename_file.kwargs import RenameFileKwargs
from functions.file_management.file_operations import save_file


def rename_file(args_dict: ArgsDict) -> ExecutionResult:
    new_name = args_dict.get_kwarg(RenameFileKwargs.NewName)[0] + ".mp3"
    file = args_dict.get_file()
    file.filename = new_name
    print(new_name)
    quit()

    if file.db_file is not None:
        try:
            os.rename(file.path, file.path[-len(file.filename) :] + new_name)
            save_file(file.db_file, file)
            return ExecutionResult.message("ok")  # todo rework these ok messages
        except:
            return ExecutionResult.error_message(
                "Could not rename the file. Check for illegal characters or file permissions."
            )
    else:
        file = analyze_file(file)
        cached = cache.get_files_to_import()
        if cached is not None:
            cache.set_current_file(file)
            cache.update_files_to_import(file)
