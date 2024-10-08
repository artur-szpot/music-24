from typing import Dict, List, Union

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.arg_validation_errors import ArgumentValidationError
from functions.execute.validate_args import AllowedKwarg
from functions.file_management.file_operations import save_file
from functions.music_file.MusicFile import MusicFileDbProps, MusicFile

args_validator = ArgsValidator.file_and_no_args().kwargs(
    allowed_kwargs={
        "add-authors": AllowedKwarg.any(),
        "remove-authors": AllowedKwarg.any(),
        "add-genres": AllowedKwarg.any(),
        "remove-genres": AllowedKwarg.any(),
        "authors": AllowedKwarg.any(),
        "genres": AllowedKwarg.any(),
        "title": AllowedKwarg.single(),
        "rating": AllowedKwarg.single(),
        "is_mlp": AllowedKwarg.single(),
        "is_dad": AllowedKwarg.single(),
        "is_ready": AllowedKwarg.single(),
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


def edit_file(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()

    instructions: Dict[str, Union[str, List[str], Dict[str, List[str]]]] = {}
    add: Dict[str, List[str]] = {"a": []}
    add_authors = args_dict.get_kwarg("add-authors")
    add_genres = args_dict.get_kwarg("add-genres")
    if add_authors:
        add["authors"] = add_authors
    if add_genres:
        add["genres"] = add_genres
    if len(add) > 1:
        instructions["add"] = add

    remove: Dict[str, List[str]] = {"a": []}
    remove_authors = args_dict.get_kwarg("remove-authors")
    remove_genres = args_dict.get_kwarg("remove-genres")
    if remove_authors:
        remove["authors"] = remove_authors
    if remove_genres:
        remove["genres"] = remove_genres
    if len(remove) > 1:
        instructions["remove"] = remove

    authors = args_dict.get_kwarg("authors")
    if authors:
        instructions["authors"] = authors

    genres = args_dict.get_kwarg("genres")
    if genres:
        instructions["genres"] = genres

    title = args_dict.get_kwarg("title")
    if title:
        instructions["title"] = title[0]

    rating = args_dict.get_kwarg("rating")
    if rating:
        instructions["rating"] = rating[0]

    is_mlp = args_dict.get_kwarg("is_mlp")
    if is_mlp:
        instructions["is_mlp"] = is_mlp[0]

    is_dad = args_dict.get_kwarg("is_dad")
    if is_dad:
        instructions["is_dad"] = is_dad[0]

    is_ready = args_dict.get_kwarg("is_ready")
    if is_ready:
        instructions["is_ready"] = is_ready[0]

    return edit_file_exe(file, instructions)


def edit_file_exe(file: MusicFile, instructions: Dict) -> ExecutionResult:
    if not instructions:
        raise ArgumentValidationError("No values to update provided")

    add = instructions.get("add")
    remove = instructions.get("remove")
    if add is not None:
        if "authors" in add:
            authors = file.authors
            authors += add.get("authors")
            file.authors = authors
        if "genres" in add:
            genres = file.genres
            genres += add.get("genres")
            file.genres = genres
    if remove is not None:
        if "authors" in remove:
            authors = [a for a in file.authors if a not in remove.get("authors")]
            file.authors = authors
        if "genres" in remove:
            genres = [g for g in file.genres if g not in remove.get("genres")]
            file.genres = genres
    if "authors" in instructions:
        file.authors = instructions["authors"]
    if "genres" in instructions:
        file.genres = instructions["genres"]
    if "title" in instructions:
        file.title = instructions["title"]
    if "rating" in instructions:
        file.rating = instructions["rating"]
    if "is_mlp" in instructions:
        file.is_mlp = bool(instructions["is_mlp"])
    if "is_dad" in instructions:
        file.is_dad = bool(instructions["is_dad"])
    if "is_ready" in instructions:
        file.is_ready = bool(instructions["is_ready"])
    file.set_db_prop(MusicFileDbProps.Desynced, True)
    save_file(filename, file)  # todo continue here
    return ExecutionResult.message("ok")
