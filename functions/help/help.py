from functions.commands.CommandEnum import CommandEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.execute.ExecutionResult import ExecutionResult
from functions.help.mock_definition import mock_definition

categories = {
    FunctionCategoryEnum.AppManagement: "App management",
    FunctionCategoryEnum.ViewingFiles: "View files",
    FunctionCategoryEnum.EditingFiles: "Edit files",
    FunctionCategoryEnum.IngestingFiles: "Ingest new files",
    FunctionCategoryEnum.CreatingPlaylists: "Create playlists",
    FunctionCategoryEnum.ExportingFiles: "Export files",
    FunctionCategoryEnum.Unassigned: "WIP, not yet described",
}


def print_help(args_dict: ArgsDict) -> ExecutionResult:
    command_registry = args_dict.system["command_registry"]
    help_contents = []
    all_commands = [
        command_registry.get(command, mock_definition()) for command in CommandEnum
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
    return ExecutionResult.table(header=[], items=help_contents)
