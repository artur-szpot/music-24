from typing import Dict

from functions.commands.CommandEnum import CommandEnum
from functions.commands.ExitCommand import exit_definition
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.functions.command_add.definition import add_definition
from functions.data_types.functions.command_add_variant.definition import (
    add_variant_definition,
)
from functions.file_import.analyze.command_fix.definition import fix_definition
from functions.file_import.analyze.command_import_files.definition import (
    import_files_definition,
)
from functions.file_import.analyze.command_print_file_analysis.definition import (
    print_file_analysis_definition,
)
from functions.file_management.command_clear_db.definition import clear_db_definition
from functions.file_management.command_edit_file.definition import edit_file_definition
from functions.file_management.command_rename_file.definition import (
    rename_file_definition,
)
from functions.help.command_help.definition import help_definition
from functions.log.command_show_log.definition import show_log_definition
from functions.querying.command_detail_view.definition import detail_view_definition
from functions.querying.command_list_all_files.definition import (
    list_all_files_definition,
)
from functions.result_scrolling.command_next_page.definition import next_page_definition
from functions.result_scrolling.command_previous_page.definition import (
    previous_page_definition,
)
from functions.result_scrolling.command_set_page_number.definition import (
    set_page_number_definition,
)
from functions.settings.text_color.command_set_color_scheme.definition import (
    set_color_scheme_definition,
)
from functions.settings.text_color.command_set_page_size.definition import (
    set_page_size_definition,
)

command_registry: Dict[CommandEnum, FunctionDefinition] = {
    CommandEnum.Exit: exit_definition(),
    CommandEnum.ShowLog: show_log_definition(),
    # ===================
    CommandEnum.ListFiles: list_all_files_definition(),
    CommandEnum.FileDetails: detail_view_definition(),
    CommandEnum.EditDatabaseFile: edit_file_definition(),
    # CommandEnum.UpdateFromMp3: update_from_mp3,
    # CommandEnum.UpdateFromDatabase: update_from_database,
    # ===================
    CommandEnum.AnalyzeImport: print_file_analysis_definition(),
    CommandEnum.Fix: fix_definition(),
    CommandEnum.ImportFiles: import_files_definition(),
    CommandEnum.RenameFile: rename_file_definition(),
    # ===================
    #     CommandEnum.ListArtists:
    CommandEnum.AddArtist: add_definition(DataTypeEnum.ARTIST),
    #     CommandEnum.RenameArtist:
    CommandEnum.AddArtistAlias: add_variant_definition(DataTypeEnum.ARTIST, True),
    #     CommandEnum.RemoveArtistAlias:
    #     CommandEnum.PromoteArtistAlias:
    CommandEnum.AddArtistMisspelling: add_variant_definition(
        DataTypeEnum.ARTIST, False
    ),
    #     CommandEnum.RemoveArtistMisspelling:
    #     CommandEnum.PromoteArtistMisspelling:
    # ===================
    #     CommandEnum.ListGenres:
    CommandEnum.AddGenre: add_definition(DataTypeEnum.GENRE),
    #     CommandEnum.RenameGenre:
    CommandEnum.AddGenreAlias: add_variant_definition(DataTypeEnum.GENRE, True),
    #     CommandEnum.RemoveGenreAlias:
    #     CommandEnum.PromoteGenreAlias:
    CommandEnum.AddGenreMisspelling: add_variant_definition(DataTypeEnum.GENRE, False),
    #     CommandEnum.RemoveGenreMisspelling:
    #     CommandEnum.PromoteGenreMisspelling:
    # ===================
    CommandEnum.Help: help_definition(),
    # ===================
    CommandEnum.NextPage: next_page_definition(),
    CommandEnum.PreviousPage: previous_page_definition(),
    CommandEnum.SetPageNumber: set_page_number_definition(),
    CommandEnum.SetPageSize: set_page_size_definition(),
    # ===================
    CommandEnum.ClearDatabase: clear_db_definition(),
    # ===================
    CommandEnum.SetColorScheme: set_color_scheme_definition(),
}
