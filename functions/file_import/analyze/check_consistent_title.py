from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_consistent_title(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    if file.ignore_predicted_filename_differences[
        IgnoreFilenameDifferences.CONSISTENT_TITLE
    ]:
        return None
    if file.title == file.predicted_title:
        return None
    fixes = []
    if len(file.predicted_title):
        fixes.append(
            MusicFileErrorFix(
                f"Use title from file name ({file.predicted_title})",
                f"edit-file {ordinal} --title {quoted(file.predicted_title)}",
            )
        )
    # todo add possibility to change file name instead
    return analysis(
        errors=MusicFileError("Title in tags differs from the one in file name", fixes)
    )
