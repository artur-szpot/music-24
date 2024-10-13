from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix


def check_any_genres_set(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    if not len(file.genres):
        return analysis(errors=MusicFileError(
            "No genres in tags",
            MusicFileErrorFix.with_user_input(
                "Add genres...",
                f"edit-file {ordinal} --genres ",
            ),
        ),
        )
        # todo FUTURE play the file and set values in the app itself
