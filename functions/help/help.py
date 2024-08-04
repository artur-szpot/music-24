from enums.commands import CommandEnum, command_registry
from enums.function_categories import FunctionCategoryEnum
from functions.execute.ArgsDict import ArgsDict
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.help.help_help import mock_help

categories = {
    FunctionCategoryEnum.AppManagement: "App management",
    FunctionCategoryEnum.ViewingFiles: "View files",
    FunctionCategoryEnum.EditingFiles: "Edit files",
    FunctionCategoryEnum.IngestingFiles: "Ingest new files",
    FunctionCategoryEnum.CreatingPlaylists: "Create playlists",
    FunctionCategoryEnum.ExportingFiles: "Export files",
    FunctionCategoryEnum.Unassigned: "WIP, not yet described",
}


def print_help(args_dict: ArgsDict):
    ArgsExtractor.no_args(args_dict)
    help_contents = []
    all_commands = [
        command_registry.get(command, mock_help()) for command in CommandEnum
    ]
    for category in FunctionCategoryEnum:
        commands = list(
            filter(lambda command: command.category == category, all_commands)
        )
        if not commands:
            continue
        help_contents.append(f"====== {categories.get(category)} ======")
        for command in commands:
            help_contents.append(f"{', '.join(command.verbs)}: {command.description}")
    return help_contents
