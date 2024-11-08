from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator

from functions.settings.text_color.command_set_page_size.executor import set_page_size
from functions.settings.text_color.command_set_page_size.flags import (
    set_page_size_flags,
)
from functions.settings.text_color.command_set_page_size.verbs import set_page_size_verbs


def set_page_size_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_page_size,
        verbs=set_page_size_verbs,
        args_validator=ArgsValidator.args(max=1).flags(set_page_size_flags),
        description="Check or set the number of results to appear on a page",
        category=FunctionCategoryEnum.AppSettings,
    )
