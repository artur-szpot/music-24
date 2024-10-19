from enum import Enum


class EditFileKwargs(Enum):
    AddArtists = "add-artists"
    RemoveArtists = "remove-artists"
    AddGenres = "add-genres"
    RemoveGenres = "remove-genres"
    Artists = "artists"
    Genres = "genres"
    Title = "title"
    Rating = "rating"
    IsMLP = "is_mlp"
    IsDad = "is_dad"
    IsReady = "is_ready"
    Ignore = "ignore"
