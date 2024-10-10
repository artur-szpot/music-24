from typing import Dict

from functions.commands.CommandEnum import CommandEnum
from functions.commands.ExitCommand import exit_definition
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.functions.add import add_definition
from functions.file_import.fix import fix_definition
from functions.file_import.print_file_analysis import print_file_analysis_definition
from functions.file_management.clear_db import clear_db_definition
from functions.file_management.edit_file import edit_file_definition
from functions.file_import.import_files import (
    import_files_definition,
)
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.help.help_definition import help_definition
from functions.querying.detail_view import print_detail_view_definition
from functions.querying.list_files import list_all_files_definition
from functions.result_scrolling.next_page import next_page_definition
from functions.result_scrolling.previoust_page import previous_page_definition
from functions.result_scrolling.set_page_number import set_page_number_definition
from functions.settings.text_color.set_color_scheme import set_color_scheme_definition
from functions.settings.set_page_size import set_page_size_definition

command_registry: Dict[CommandEnum, FunctionDefinition] = {
    CommandEnum.Exit: exit_definition(),
    CommandEnum.Help: help_definition(),
    CommandEnum.ListFiles: list_all_files_definition(),
    CommandEnum.ImportFiles: import_files_definition(),
    CommandEnum.AnalyzeImport: print_file_analysis_definition(),
    CommandEnum.EditDatabaseFile: edit_file_definition(),
    CommandEnum.SetPageSize: set_page_size_definition(),
    CommandEnum.SetPageNumber: set_page_number_definition(),
    CommandEnum.SetColorScheme: set_color_scheme_definition(),
    CommandEnum.NextPage: next_page_definition(),
    CommandEnum.PreviousPage: previous_page_definition(),
    CommandEnum.ClearDatabase: clear_db_definition(),
    CommandEnum.FileDetails: print_detail_view_definition(),
    CommandEnum.Fix: fix_definition(),
    CommandEnum.AddArtist: add_definition(DataTypeEnum.ARTIST),
    CommandEnum.AddGenre: add_definition(DataTypeEnum.GENRE),
    # CommandEnum.UpdateFromDatabase: update_from_database,
    # CommandEnum.UpdateFromMp3: update_from_mp3,
}
