from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.result_scrolling.command_set_page_number.executor import set_page_number


def set_page_number_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_page_number,
        verbs=["page", "p"],
        args_validator=ArgsValidator.args(exact=1),
        description="Move to a given page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )
