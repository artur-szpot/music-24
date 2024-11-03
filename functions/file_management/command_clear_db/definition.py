from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.file_management.command_clear_db.executor import clear_db
from functions.file_management.command_clear_db.verbs import clear_db_verbs


def clear_db_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=clear_db,
        verbs=clear_db_verbs,
        args_validator=ArgsValidator.no_args(),
        description="Remove all the saved information from the database.",
        category=FunctionCategoryEnum.EditingFiles,
    )
