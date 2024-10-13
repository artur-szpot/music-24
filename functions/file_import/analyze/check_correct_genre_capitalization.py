from typing import Optional

from functions.data_types.Genre import Genre
from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_correct_genre_capitalization(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    warnings = []
    for genre in file.genres:
        correct_capitalization = Genre.check_capitalization(genre)
        if correct_capitalization is not None:
            warnings.append(
                MusicFileError(
                    f"Wrong genre name capitalization: {genre}",
                    [
                        MusicFileErrorFix(
                            f"Change the capitalization to {correct_capitalization}",
                            f"edit-file {ordinal} --remove-genres {quoted(genre)} "
                            f"--add-genres {quoted(correct_capitalization)}",
                        ),
                        MusicFileErrorFix.with_user_input(
                            f"Rename the genre...",
                            f"edit-file {ordinal} --remove-genres {quoted(genre)} "
                            f"--add-genres ",
                        ),
                    ],
                )
            )
    return analysis(warnings=warnings)
