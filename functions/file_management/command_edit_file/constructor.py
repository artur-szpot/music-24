from typing import List

from functions.commands.print_command import print_command
from functions.file_management.command_edit_file.kwargs import (
    EditFileKwargs,
    edit_file_kwargs,
)
from functions.file_management.command_edit_file.verbs import edit_file_verbs
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences


class EditFileCommand:
    @staticmethod
    def create(
        ordinal: int,
        add_artists: List[str] = None,
        add_genres: List[str] = None,
        remove_artists: List[str] = None,
        remove_genres: List[str] = None,
        artists: List[str] = None,
        genres: List[str] = None,
        title: str = None,
        rating: int = None,
        is_mlp: bool = None,
        is_dad: bool = None,
        is_ready: bool = None,
        ignore: List[IgnoreFilenameDifferences] = None,
    ) -> str:
        kwargs = []
        if add_artists:
            kwargs.append({EditFileKwargs.AddArtists: add_artists})
        if add_genres:
            kwargs.append({EditFileKwargs.AddGenres: add_genres})
        if remove_artists:
            kwargs.append({EditFileKwargs.RemoveArtists: remove_artists})
        if remove_genres:
            kwargs.append({EditFileKwargs.RemoveGenres: remove_genres})
        if artists:
            kwargs.append({EditFileKwargs.Artists: artists})
        if genres:
            kwargs.append({EditFileKwargs.Genres: genres})
        if title:
            kwargs.append({EditFileKwargs.Title: title})
        if rating:
            kwargs.append({EditFileKwargs.Rating: rating})
        if is_mlp:
            kwargs.append({EditFileKwargs.IsMLP: "1" if is_mlp else "0"})
        if is_dad:
            kwargs.append({EditFileKwargs.IsDad: "1" if is_dad else "0"})
        if is_ready:
            kwargs.append({EditFileKwargs.IsReady: "1" if is_ready else "0"})
        if ignore:
            kwargs.append({EditFileKwargs.Ignore: [i.value for i in ignore]})
        return print_command(
            edit_file_verbs,
            args=[str(ordinal)],
            kwargs=kwargs,
            kwarg_dict=edit_file_kwargs,
        )
