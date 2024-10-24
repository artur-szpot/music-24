from typing import Dict, List, Tuple

from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.data_types.ArtistRole import ArtistRole
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.execute.validate.arg_validation_errors import ArgumentValidationError
from functions.file_import.analyze.analyze_files import analyze_file
from functions.file_management.command_edit_file.kwargs import (
    EditFileKwargs,
    edit_file_kwargs,
)
from functions.file_management.file_operations import save_file
from functions.music_file.MusicFile import MusicFileDbProps, MusicFile
from libs.strings import quoted


def edit_file(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()

    instructions: dict = {}
    add: Dict[str, List[str]] = {"a": []}
    add_artists = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.AddArtists))
    add_genres = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.AddGenres))
    if add_artists:
        add["artists"] = add_artists
    if add_genres:
        add["genres"] = add_genres
    if len(add) > 1:
        instructions["add"] = add

    remove: Dict[str, List[str]] = {"a": []}
    remove_artists = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.RemoveArtists))
    remove_genres = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.RemoveGenres))
    if remove_artists:
        remove["artists"] = remove_artists
    if remove_genres:
        remove["genres"] = remove_genres
    if len(remove) > 1:
        instructions["remove"] = remove

    artists = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.Artists))
    if artists:
        instructions["artists"] = artists

    genres = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.Genres))
    if genres:
        instructions["genres"] = genres

    title = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.Title))
    if title:
        instructions["title"] = title[0]

    rating = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.Rating))
    if rating:
        instructions["rating"] = int(rating[0])

    is_mlp = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.IsMLP))
    if is_mlp:
        instructions["is_mlp"] = is_mlp[0]

    is_dad = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.IsDad))
    if is_dad:
        instructions["is_dad"] = is_dad[0]

    is_ready = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.IsReady))
    if is_ready:
        instructions["is_ready"] = is_ready[0]

    ignore = args_dict.get_kwarg(edit_file_kwargs(EditFileKwargs.Ignore))
    if ignore:
        instructions["ignore"] = ignore[0]

    return edit_file_exe(file, instructions)


def map_artist_input(file: MusicFile, value: str) -> None:
    artists_to_add: List[Tuple[str, List[ArtistRole]]] = []
    for artist in value:
        if artist in ["main", "m"]:
            pass
        elif artist in ["orig", "o", "original"]:
            if not len(artists_to_add):
                raise ValueError(f"Illegal artist name supplied: {artist}")
            artists_to_add[-1][1].append(ArtistRole.Original)
        elif artist in ["feat", "f", "featuring"]:
            if not len(artists_to_add):
                raise ValueError(f"Illegal artist name supplied: {artist}")
            artists_to_add[-1][1].append(ArtistRole.Feat)
        else:
            artists_to_add.append((artist, []))
    for artist in artists_to_add:
        roles = artist[1]
        if not len(roles):
            roles = [ArtistRole.Original]
        elif ArtistRole.Original in roles and ArtistRole.Remixer in roles:
            raise ValueError(
                f"Artist {quoted(artist[0])} cannot be both a remixer and original"
            )
        file.artists.update({artist[0]: roles})


def edit_file_exe(file: MusicFile, instructions: dict) -> ExecutionResult:
    if not instructions:
        raise ArgumentValidationError("No values to update provided")

    add = instructions.get("add")
    remove = instructions.get("remove")
    if add is not None:
        if "artists" in add:
            map_artist_input(file, add.get("artists"))
        if "genres" in add:
            genres = add.get("genres") + file.genres
            file.genres = genres
    if remove is not None:
        if "artists" in remove:
            for a in remove.get("artists"):
                if a in file.artists:
                    del file.artists[a]
        if "genres" in remove:
            genres = [g for g in file.genres if g not in remove.get("genres")]
            file.genres = genres
    if "artists" in instructions:
        file.artists = {}
        map_artist_input(file, instructions["artists"])
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
    if "ignore" in instructions:
        file.ignore_predicted_filename_differences[instructions["ignore"]] = True
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
