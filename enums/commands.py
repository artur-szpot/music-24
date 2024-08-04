from enum import Enum

from enums.function_categories import FunctionCategoryEnum
from functions.file_management.edit_db_file import edit_db_file_help
from functions.file_management.import_files import (
    import_files_help,
    print_file_analysis_help,
)
from functions.help.FunctionHelp import FunctionHelp
from functions.help.help_help import help_help
from functions.querying.list_files import list_all_files_help


class CommandEnum(Enum):
    Exit = 0  # close the app
    ListFiles = 2  # list the files in the file_management
    # View = 3  # set how the list view is presented
    # view lAt = length author(sort by) title
    # ["view", "v"],
    ImportFiles = 4  # look through the files in the directory set for importing from, add them to file_management and move to proper storage folder
    EditDatabaseFile = 5  # change whatever values for the file in database
    UpdateFromMp3 = 6  # set database values from mp3 file
    UpdateFromDatabase = 7  # set mp3 values from database file
    # query for files with given properties (can give return size, then random)
    # save query results as albums or playlists
    # export query results/albums/playlists in different formats (win, car, ?)
    # save info about what has been exported (i.e. listened to)
    AnalyzeImport = 8  # analyze files before importing them
    # organize files (compile files, dictify artists, genres)
    # create indexes for faster access?
    # continuous command mode (ls -> next; edit -> author)
    # stats
    # set artist/genre alt-names
    # set artist/genre misspellings and use them to correct saved data
    # rewrite artist/genre from one value to another
    Help = 9


def exit_help() -> FunctionHelp:
    return FunctionHelp(
        ["exit", "x"],
        "Closes the application.",
        FunctionCategoryEnum.AppManagement,
    )


command_registry = {
    CommandEnum.Exit: exit_help(),
    CommandEnum.Help: help_help(),
    CommandEnum.ListFiles: list_all_files_help(),
    CommandEnum.ImportFiles: import_files_help(),
    CommandEnum.AnalyzeImport: print_file_analysis_help(),
    CommandEnum.EditDatabaseFile: edit_db_file_help(),
    # CommandEnum.UpdateFromDatabase: update_from_database,
    # CommandEnum.UpdateFromMp3: update_from_mp3,
}


def get_command_dictionary():
    command_dictionary = {}

    for command in command_registry:
        for code in command_registry[command].verbs:
            if code in command_dictionary:
                raise KeyError(f"Repeated code {code} detected")
            command_dictionary[code] = command

    return command_dictionary
