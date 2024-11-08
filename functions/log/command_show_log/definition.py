from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.log.command_show_log.executor import show_log
from functions.log.command_show_log.verbs import show_log_verbs


def show_log_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=show_log,
        verbs=show_log_verbs,
        args_validator=ArgsValidator.no_args(),
        description="Shows the last few executed commands.",
        category=FunctionCategoryEnum.AppManagement,
    )
