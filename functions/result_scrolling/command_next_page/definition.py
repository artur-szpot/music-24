from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.result_scrolling.command_next_page.executor import next_page
from functions.result_scrolling.command_next_page.verbs import next_page_verbs


def next_page_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=next_page,
        verbs=next_page_verbs,
        args_validator=ArgsValidator.no_args(),
        description="Move to the next page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )
