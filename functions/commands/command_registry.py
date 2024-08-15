from typing import Dict

from functions.commands.CommandEnum import CommandEnum
from functions.commands.ExitCommand import exit_definition
from functions.file_management.clear_db import clear_db_definition
from functions.file_management.edit_db_file import edit_db_file_definition
from functions.file_management.import_files import (
    import_files_definition,
    print_file_analysis_definition,
)
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.help.help_definition import help_definition
from functions.querying.list_files import list_all_files_definition
from functions.result_scrolling.next_page import next_page_definition
from functions.result_scrolling.previoust_page import previous_page_definition
from functions.result_scrolling.set_page_number import set_page_number_definition
from functions.settings.set_page_size import set_page_size_definition

command_registry: Dict[CommandEnum, FunctionDefinition] = {
    CommandEnum.Exit: exit_definition(),
    CommandEnum.Help: help_definition(),
    CommandEnum.ListFiles: list_all_files_definition(),
    CommandEnum.ImportFiles: import_files_definition(),
    CommandEnum.AnalyzeImport: print_file_analysis_definition(),
    CommandEnum.EditDatabaseFile: edit_db_file_definition(),
    CommandEnum.SetPageSize: set_page_size_definition(),
    CommandEnum.SetPageNumber: set_page_number_definition(),
    CommandEnum.NextPage: next_page_definition(),
    CommandEnum.PreviousPage: previous_page_definition(),
    CommandEnum.ClearDatabase: clear_db_definition(),
    # CommandEnum.UpdateFromDatabase: update_from_database,
    # CommandEnum.UpdateFromMp3: update_from_mp3,
}
