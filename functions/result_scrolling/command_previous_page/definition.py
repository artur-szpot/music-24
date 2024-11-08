from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.result_scrolling.command_previous_page.executor import previous_page
from functions.result_scrolling.command_previous_page.verbs import previous_page_verbs


def previous_page_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=previous_page,
        verbs=previous_page_verbs,
        args_validator=ArgsValidator.no_args(),
        description="Move to the previous page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )
