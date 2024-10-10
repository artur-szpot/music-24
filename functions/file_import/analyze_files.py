from typing import List, Optional

from functions.data_types.artist_registry import artist_registry
from functions.data_types.genre_registry import genre_registry
from functions.file_import.read_files_to_import import read_files_to_import
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def analyze_files(
    show_only_if_error: bool = False,
    show_only_if_warning: bool = False,
    overwrite_cache: bool = False,
) -> List[MusicFile]:
    files = read_files_to_import(overwrite_cache)
    files_to_show = []
    for index, file in enumerate(files):
        file.set_view_props(index)
        checked_file = analyze_file(file, show_only_if_error, show_only_if_warning)
        if checked_file is not None:
            files_to_show.append(checked_file)
    return files_to_show


def analyze_file(
    file: MusicFile,
    show_only_if_error: bool = False,
    show_only_if_warning: bool = False,
) -> Optional[MusicFile]:
    # skip if the file is a front for wrong format
    if not file.length:
        return file

    errors: List[MusicFileError] = []
    warnings: List[MusicFileError] = []
    ordinal = file.get_ordinal_number()

    if not len(file.artists):
        fixes = []
        if file.predicted_artists:
            fixes.append(
                MusicFileErrorFix(
                    f"Add artists based on file name: {', '.join(file.predicted_artists)}",
                    f"edit-file {ordinal} --artists {' '.join(quoted(artist) for artist in file.predicted_artists)}",
                )
            )
        fixes.append(
            MusicFileErrorFix.with_user_input(
                "Add artists...",
                f"edit-file {ordinal} --artists ",
            )
        )
        errors.append(MusicFileError("No artists in tags", fixes))

    for artist in file.artists:
        if "," in artist or "[" in artist or "]" in artist:
            corrected_artist = (
                artist.replace(",", "").replace("[,]", "").replace("]", "")
            )
            errors.append(
                MusicFileError(
                    f"Artist with illegal symbols in their name: {artist}",
                    [
                        MusicFileErrorFix(
                            f"Change artist name to {corrected_artist}",
                            f"edit-file {ordinal} --remove-artists {quoted(artist)} "
                            f"--add-artists {quoted(corrected_artist)}",
                        ),
                        MusicFileErrorFix.with_user_input(
                            f"Change artist name to...",
                            f"edit-file {ordinal} --remove-artists {quoted(artist)} --add-artists ",
                        ),
                    ],
                )
            )

        if artist not in file.predicted_artists:
            errors.append(MusicFileError(f"Artist missing from file name: {artist}"))
            # alias existing artist to {}
            # replace existing artist
            # todo command to change file name
            # todo command to alias artists

        if not artist_registry.find(artist):
            warnings.append(
                MusicFileError(
                    f"New artist: {artist}",
                    [
                        MusicFileErrorFix(
                            f"Add new artist",
                            f"add-artist {quoted(artist)}",
                        ),
                    ],
                )
            )
            # todo
            # alias existing artist to {}
            # replace existing artist

    for artist in file.predicted_artists:
        # alias existing artist to {}
        # replace existing artist
        if artist not in file.artists:
            errors.append(
                MusicFileError(
                    f"Artist missing from tags: {artist}",
                    MusicFileErrorFix(
                        "Add artist to tags",
                        f"edit-file {ordinal} --add-artists {quoted(artist)}",
                    ),
                )
            )

    if not len(file.genres):
        errors.append(
            MusicFileError(
                "No genres in tags",
                MusicFileErrorFix.with_user_input(
                    "Add genres...",
                    f"edit-file {ordinal} --genres ",
                ),
            ),
        )
        # todo FUTURE play the file and set values in the app itself

    for genre in file.genres:
        if "," in genre:
            corrected_genre = genre.replace(",", "")
            # todo command to alias genres [genres will autocorrect, artists will not]
            # alias existing genre to {}
            # replace existing genre
            errors.append(
                MusicFileError(
                    f"Genre with illegal symbols in their name: {genre}",
                    [
                        MusicFileErrorFix(
                            f"Change genre to {corrected_genre}",
                            f"edit-file {ordinal} --remove-genres {quoted(genre)} --add-genres {quoted(corrected_genre)}",
                        ),
                        MusicFileErrorFix.with_user_input(
                            f"Change genre to...",
                            f"edit-file {ordinal} --remove-genres {quoted(genre)} --add-genres ",
                        ),
                    ],
                )
            )

        if not genre_registry.find(genre):
            warnings.append(
                MusicFileError(
                    f"New genre: {genre}",
                    [
                        MusicFileErrorFix(
                            f'Add new "music type" genre',
                            f"add-genre {quoted(genre)} --category type",
                        ),
                        MusicFileErrorFix(
                            f'Add new "music genre" genre',
                            f"add-genre {quoted(genre)} --category genre",
                        ),
                        MusicFileErrorFix(
                            f'Add new "music quality" genre',
                            f"add-genre {quoted(genre)} --category quality",
                        ),
                    ],
                )
            )
            # todo command to alias genres [genres will autocorrect, artists will not]

        correct_capitalization = " ".join(
            [word[0].upper() + word[1:].lower() for word in genre.split(" ")]
        )
        if genre != correct_capitalization:
            warnings.append(
                MusicFileError(
                    f"Wrong genre name capitalization: {genre}",
                    MusicFileErrorFix(
                        f"Change the capitalization to {correct_capitalization}",
                        f"edit-file {ordinal} --remove-genres {quoted(genre)} "
                        f"--add-genres {quoted(correct_capitalization)}",
                    ),
                )
            )

    if not len(file.title):
        fixes = []
        if len(file.predicted_title):
            fixes.append(
                MusicFileErrorFix(
                    f"Use title from file name ({file.predicted_title})",
                    f"edit-file {ordinal} --title {quoted(file.predicted_title)}",
                )
            )
        errors.append(MusicFileError("No title set", fixes))

    if file.title != file.predicted_title:
        fixes = []
        if len(file.predicted_title):
            fixes.append(
                MusicFileErrorFix(
                    f"Use title from file name ({file.predicted_title})",
                    f"edit-file {ordinal} --title {quoted(file.predicted_title)}",
                )
            )
        # todo add possibility to change file name instead
        errors.append(
            MusicFileError("Title in tags differs from the one in file name", fixes)
        )

    if file.rating is None or file.rating < 0 or file.rating > 10:
        errors.append(
            MusicFileError(
                f"Invalid file rating: {file.rating}",
                MusicFileErrorFix.rating_options(ordinal),
            )
        )

    if file.rating == 0:
        errors.append(
            MusicFileError(
                "File rating not set",
                MusicFileErrorFix.rating_options(ordinal),
            )
        )

    if file.is_dad is None:
        errors.append(
            MusicFileError(
                "Dad flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_dad"),
            )
        )

    if file.is_mlp is None:
        errors.append(
            MusicFileError(
                "MLP flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_mlp"),
            )
        )

    if file.is_ready is None:
        errors.append(
            MusicFileError(
                "Ready flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_ready"),
            )
        )

    # todo check for additional leftover tags
    # todo check for comments (including allowed ones)
    # todo record edit needed tag
    # todo check for image
    # todo check for type (sometimes incorrectly set as Classical etc.)

    file.errors = errors
    file.warnings = warnings

    if (
        not (show_only_if_error or show_only_if_warning)
        or (show_only_if_error and len(file.errors))
        or (show_only_if_warning and len(file.warnings))
    ):
        return file

    return None
