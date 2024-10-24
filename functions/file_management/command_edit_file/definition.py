from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.validate.validate_args import KwargDefinition
from functions.file_management.command_edit_file.executor import edit_file
from functions.file_management.command_edit_file.kwargs import (
    EditFileKwargs,
    edit_file_kwargs,
)

args_validator = ArgsValidator.file_and_no_args().kwargs(
    allowed_kwargs={
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.AddArtists)),
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.RemoveArtists)),
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.AddGenres)),
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.RemoveGenres)),
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.Artists)),
        KwargDefinition.any(edit_file_kwargs(EditFileKwargs.Genres)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.Title)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.Rating)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.IsMLP)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.IsDad)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.IsReady)),
        KwargDefinition.single(edit_file_kwargs(EditFileKwargs.Ignore)),
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
