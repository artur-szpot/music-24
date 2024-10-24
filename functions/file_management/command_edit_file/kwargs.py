from enum import Enum

from libs.list_union_util import SimpleList


class EditFileKwargs(Enum):
    AddArtists = 0
    RemoveArtists = 1
    AddGenres = 2
    RemoveGenres = 3
    Artists = 4
    Genres = 5
    Title = 6
    Rating = 7
    IsMLP = 8
    IsDad = 9
    IsReady = 10
    Ignore = 11


def edit_file_kwargs(value: EditFileKwargs) -> SimpleList[str]:
    return {
        EditFileKwargs.AddArtists: ["add-artists"],
        EditFileKwargs.RemoveArtists: ["remove-artists"],
        EditFileKwargs.AddGenres: ["add-genres"],
        EditFileKwargs.RemoveGenres: ["remove-genres"],
        EditFileKwargs.Artists: ["artists"],
        EditFileKwargs.Genres: ["genres"],
        EditFileKwargs.Title: ["title"],
        EditFileKwargs.Rating: ["rating"],
        EditFileKwargs.IsMLP: ["is_mlp"],
        EditFileKwargs.IsDad: ["is_dad"],
        EditFileKwargs.IsReady: ["is_ready"],
        EditFileKwargs.Ignore: ["ignore"],
    }.get(value, [])
