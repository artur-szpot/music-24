from typing import List, Optional, Callable

from functions.file_import.analyze.analysis_helpers import AnalysisResult
from functions.file_import.analyze.check_any_artists_set import check_any_artists_set
from functions.file_import.analyze.check_any_genres_set import check_any_genres_set
from functions.file_import.analyze.check_artists_missing_from_filename import (
    check_artists_missing_from_filename,
)
from functions.file_import.analyze.check_artists_missing_from_tags import (
    check_artists_missing_from_tags,
)
from functions.file_import.analyze.check_consistent_filename import (
    check_consistent_filename,
)
from functions.file_import.analyze.check_consistent_filename_after_corrections import (
    check_consistent_filename_after_corrections,
)
from functions.file_import.analyze.check_consistent_title import check_consistent_title
from functions.file_import.analyze.check_correct_genre_capitalization import (
    check_correct_genre_capitalization,
)
from functions.file_import.analyze.check_flag_tags import check_flag_tags
from functions.file_import.analyze.check_illegal_artist_names import (
    check_illegal_artist_names,
)
from functions.file_import.analyze.check_illegal_genre_names import (
    check_illegal_genre_names,
)
from functions.file_import.analyze.check_new_artists import check_new_artists
from functions.file_import.analyze.check_new_genres import check_new_genres
from functions.file_import.analyze.check_rating import check_rating
from functions.file_import.analyze.check_repeated_genres_and_artists import (
    check_repeated_genres_and_artists,
)
from functions.file_import.analyze.check_title_set import check_title_set
from functions.file_import.read_files_to_import import read_files_to_import
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError


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

    def apply(analyzer: Callable[[MusicFile, int], Optional[AnalysisResult]]) -> None:
        result = analyzer(file, ordinal)
        if result is None:
            return
        new_errors, new_warnings = result
        errors.extend(new_errors)
        warnings.extend(new_warnings)

    # 1. Check wrong values in tags
    apply(check_illegal_artist_names)
    apply(check_illegal_genre_names)
    apply(check_correct_genre_capitalization)
    apply(check_repeated_genres_and_artists)
    apply(check_rating)

    # 2. Check that tags are set
    apply(check_flag_tags)
    apply(check_any_artists_set)
    apply(check_any_genres_set)
    # todo remove repeated genres silently (requires dictification!)
    apply(check_title_set)
    # rating done already
    # todo check for type (sometimes incorrectly set as Classical etc.)

    # 3. Check that garbage was removed
    # todo check for additional leftover tags
    # todo check for comments (including allowed ones)
    # todo check for image

    # 4. Check tags are consistent with filename - ignorable!
    apply(check_consistent_filename)
    # check mismatched artists
    # Intentionally no check for consistency of artist roles - there's no information
    # about such in the file itself and will be set upon import.
    apply(check_artists_missing_from_tags)
    apply(check_artists_missing_from_filename)
    apply(check_consistent_title)
    apply(check_consistent_filename_after_corrections)

    # 5. Expand the data types
    apply(check_new_artists)
    apply(check_new_genres)

    # todo record edit needed tag

    file.errors = errors
    file.warnings = warnings

    if (
        not (show_only_if_error or show_only_if_warning)
        or (show_only_if_error and len(file.errors))
        or (show_only_if_warning and len(file.warnings))
    ):
        return file

    return None
