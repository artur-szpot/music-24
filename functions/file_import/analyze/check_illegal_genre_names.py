from typing import Optional

from functions.data_types.Genre import Genre
from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_illegal_genre_names(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    errors = []
    for genre in file.genres:
        corrected_genre = Genre.check_legal_name(genre)
        if corrected_genre is None:
            continue
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
    return analysis(errors=errors)
