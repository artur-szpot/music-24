from typing import Dict, List, Union

from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.arg_validation_errors import ArgumentValidationError
from functions.execute.validate_args import AllowedKwarg
from functions.file_import.analyze_files import analyze_file
from functions.file_management.file_operations import save_file
from functions.music_file.MusicFile import MusicFileDbProps, MusicFile

args_validator = ArgsValidator.file_and_no_args().kwargs(
    allowed_kwargs={
        AllowedKwarg.any("add-artists"),
        AllowedKwarg.any("remove-artists"),
        AllowedKwarg.any("add-genres"),
        AllowedKwarg.any("remove-genres"),
        AllowedKwarg.any("artists"),
        AllowedKwarg.any("genres"),
        AllowedKwarg.single("title"),
        AllowedKwarg.single("rating"),
        AllowedKwarg.single("is_mlp"),
        AllowedKwarg.single("is_dad"),
        AllowedKwarg.single("is_ready"),
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
    add_artists = args_dict.get_kwarg("add-artists")
    add_genres = args_dict.get_kwarg("add-genres")
    if add_artists:
        add["artists"] = add_artists
    if add_genres:
        add["genres"] = add_genres
    if len(add) > 1:
        instructions["add"] = add

    remove: Dict[str, List[str]] = {"a": []}
    remove_artists = args_dict.get_kwarg("remove-artists")
    remove_genres = args_dict.get_kwarg("remove-genres")
    if remove_artists:
        remove["artists"] = remove_artists
    if remove_genres:
        remove["genres"] = remove_genres
    if len(remove) > 1:
        instructions["remove"] = remove

    artists = args_dict.get_kwarg("artists")
    if artists:
        instructions["artists"] = artists

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
        if "artists" in add:
            artists = file.artists
            artists += add.get("artists")
            file.artists = artists
        if "genres" in add:
            genres = file.genres
            genres += add.get("genres")
            file.genres = genres
    if remove is not None:
        if "artists" in remove:
            artists = [a for a in file.artists if a not in remove.get("artists")]
            file.artists = artists
        if "genres" in remove:
            genres = [g for g in file.genres if g not in remove.get("genres")]
            file.genres = genres
    if "artists" in instructions:
        file.artists = instructions["artists"]
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
    if file.db_file is not None:
        file.set_db_prop(MusicFileDbProps.Desynced, True)
        save_file(file.db_file, file)
    else:
        file = analyze_file(file)
        cached = cache.get_files_to_import()
        if cached is not None:
            cache.set_current_file(file)
            cache.update_files_to_import(file)
    return ExecutionResult.message("ok")
