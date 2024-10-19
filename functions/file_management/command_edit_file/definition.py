from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.validate.validate_args import KwargDefinition
from functions.file_management.command_edit_file.executor import edit_file
from functions.file_management.command_edit_file.kwargs import EditFileKwargs

args_validator = ArgsValidator.file_and_no_args().kwargs(
    allowed_kwargs={
        KwargDefinition.any(EditFileKwargs.AddArtists),
        KwargDefinition.any(EditFileKwargs.RemoveArtists),
        KwargDefinition.any(EditFileKwargs.AddGenres),
        KwargDefinition.any(EditFileKwargs.RemoveGenres),
        KwargDefinition.any(EditFileKwargs.Artists),
        KwargDefinition.any(EditFileKwargs.Genres),
        KwargDefinition.single(EditFileKwargs.Title),
        KwargDefinition.single(EditFileKwargs.Rating),
        KwargDefinition.single(EditFileKwargs.IsMLP),
        KwargDefinition.single(EditFileKwargs.IsDad),
        KwargDefinition.single(EditFileKwargs.IsReady),
        KwargDefinition.single(EditFileKwargs.Ignore),
    }
)


def edit_file_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=edit_file,
        verbs=["edit-file", "ef"],
        args_validator=args_validator,
        description="Edit the selected properties of a file.",
        category=FunctionCategoryEnum.EditingFiles,
    )
