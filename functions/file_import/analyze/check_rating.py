from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix


def check_rating(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    if file.rating is None or file.rating < 0 or file.rating > 10:
        return analysis(errors=MusicFileError(
            f"Invalid file rating: {file.rating}",
            MusicFileErrorFix.rating_options(ordinal),
        )
        )
    elif file.rating == 0:
        return analysis(errors=MusicFileError(
            "File rating not set",
            MusicFileErrorFix.rating_options(ordinal),
        )
        )
