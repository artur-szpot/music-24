from typing import Dict

from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.ArgsDict import ArgsDict
from functions.execute.ArgsValidator import ArgsValidator, ArgsValidatorSpecial
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.arg_validation_errors import ArgumentValidationError
from functions.execute.validate_args import AllowedKwarg
from functions.file_management.MusicFile import MusicFileDbProps
from functions.file_management.file_operations import open_file, save_file
from functions.definition.FunctionDefinition import FunctionDefinition

args_validator = ArgsValidator.filename_and_no_args().kwargs(
    allowed_kwargs={
        "add-authors": AllowedKwarg.any(),
        "remove-authors": AllowedKwarg.any(),
        "add-genres": AllowedKwarg.any(),
        "remove-genres": AllowedKwarg.any(),
        "authors": AllowedKwarg.single(),
        "genres": AllowedKwarg.single(),
        "title": AllowedKwarg.single(),
        "rating": AllowedKwarg.single(),
        "is_mlp": AllowedKwarg.single(),
        "is_dad": AllowedKwarg.single(),
        "is_ready": AllowedKwarg.single(),
    }
)


def edit_db_file_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=edit_db_file,
        verbs=["edit-file", "ef"],
        args_validator=args_validator,
        description="Edit the selected properties of a file in the database.",
        category=FunctionCategoryEnum.EditingFiles,
    )


def edit_db_file(args_dict: ArgsDict) -> ExecutionResult:
    filename = args_validator.get_filename(args_dict)

    music_file = {}
    add = {}
    add_authors = args_dict.get_kwarg("add-authors")
    add_genres = args_dict.get_kwarg("add-genres")
    if add_authors:
        add["authors"] = add_authors
    if add_genres:
        add["genres"] = add_genres
    if add:
        music_file["add"] = add

    remove = {}
    remove_authors = args_dict.get_kwarg("remove-authors")
    remove_genres = args_dict.get_kwarg("remove-genres")
    if remove_authors:
        remove["authors"] = remove_authors
    if remove_genres:
        remove["genres"] = remove_genres
    if remove:
        music_file["remove"] = remove

    authors = args_dict.get_kwarg("authors")
    if authors:
        music_file["authors"] = authors[0]

    genres = args_dict.get_kwarg("genres")
    if genres:
        music_file["genres"] = genres[0]

    title = args_dict.get_kwarg("title")
    if title:
        music_file["title"] = title[0]

    rating = args_dict.get_kwarg("rating")
    if rating:
        music_file["rating"] = rating[0]

    is_mlp = args_dict.get_kwarg("is_mlp")
    if is_mlp:
        music_file["is_mlp"] = is_mlp[0]

    is_dad = args_dict.get_kwarg("is_dad")
    if is_dad:
        music_file["is_dad"] = is_dad[0]

    is_ready = args_dict.get_kwarg("is_ready")
    if is_ready:
        music_file["is_ready"] = is_ready[0]

    return edit_db_file_exe(filename, music_file)


def edit_db_file_exe(filename: str, music_file: Dict) -> ExecutionResult:
    if not music_file:
        raise ArgumentValidationError("No values to update provided")

    db_file = open_file(filename)
    add = music_file.get("add")
    remove = music_file.get("remove")
    if add is not None:
        if "authors" in add:
            authors = db_file.authors
            authors += add.get("authors")
            db_file.authors = authors
        if "genres" in add:
            genres = db_file.genres
            genres += add.get("genres")
            db_file.genres = genres
    if remove is not None:
        if "authors" in remove:
            authors = [a for a in db_file.authors if a not in remove.get("authors")]
            db_file.authors = authors
        if "genres" in remove:
            genres = [g for g in db_file.genres if g not in remove.get("genres")]
            db_file.genres = genres
    if "authors" in music_file:
        db_file.authors = music_file["authors"]
    if "genres" in music_file:
        db_file.genres = music_file["genres"]
    if "title" in music_file:
        db_file.title = music_file["title"]
    if "rating" in music_file:
        db_file.rating = music_file["rating"]
    if "is_mlp" in music_file:
        db_file.is_mlp = bool(music_file["is_mlp"])
    if "is_dad" in music_file:
        db_file.is_dad = bool(music_file["is_dad"])
    if "is_ready" in music_file:
        db_file.is_ready = bool(music_file["is_ready"])
    db_file.set_db_prop(MusicFileDbProps.Desynced, True)
    save_file(filename, db_file)
    return ExecutionResult.message("ok")
