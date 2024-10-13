from typing import Optional

from functions.data_types.Genre import Genre
from functions.data_types.genre_registry import genre_registry
from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_new_genres(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    warnings = []
    for genre in file.genres:
        if not Genre.check_legal_name(genre):
            continue
        if Genre.check_capitalization(genre) is not None:
            continue
        if genre_registry.find(genre):
            continue
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
                    MusicFileErrorFix.with_user_input(
                        f'Add as alias...',
                        f"add-genre-alias {quoted(genre)} ",
                    ),
                    MusicFileErrorFix.with_user_input(
                        f'Add as misspelling...',
                        f"add-genre-misspelling {quoted(genre)} ",
                    ),
                ],
            )
        )
    return analysis(warnings=warnings)
