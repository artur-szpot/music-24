from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_consistent_filename(
    file: MusicFile, ordinal: int
) -> Optional[AnalysisResult]:
    if file.ignore_predicted_filename_differences[
        IgnoreFilenameDifferences.CONSISTENT_FILENAME
    ]:
        return None
    predicted_filename = file.create_filename()
    if file.filename[:-4] != predicted_filename:
        return analysis(
            errors=MusicFileError(
                "File name differs from expected",
                [
                    MusicFileErrorFix(
                        f"Change file name to expected: {quoted(predicted_filename)}",
                        f"rename-file {ordinal} --to {quoted(predicted_filename)}",
                    ),
                    MusicFileErrorFix(
                        "Ignore",
                        f"edit-file {ordinal} "
                        f"--ignore {IgnoreFilenameDifferences.CONSISTENT_FILENAME.value}",
                    ),
                ],
            )
        )
