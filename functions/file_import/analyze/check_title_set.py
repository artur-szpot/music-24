from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_title_set(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    if not len(file.title):
        fixes = []
        if len(file.predicted_title):
            fixes.append(
                MusicFileErrorFix(
                    f"Use title from file name ({file.predicted_title})",
                    f"edit-file {ordinal} --title {quoted(file.predicted_title)}",
                )
            )
        return analysis(errors=MusicFileError("No title set", fixes))
