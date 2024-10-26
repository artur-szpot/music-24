from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.file_management.command_edit_file.constructor import EditFileCommand
from functions.file_management.command_rename_file.constructor import RenameFileCommand
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_consistent_filename_after_corrections(
    file: MusicFile, ordinal: int
) -> Optional[AnalysisResult]:
    if not file.ignore_predicted_filename_differences[
        IgnoreFilenameDifferences.CONSISTENT_FILENAME
    ]:
        return None
    ignore_flags = [
        "mismatched_artists",
        "artists_missing_from_tags",
        "artists_missing_from_filename",
        "consistent_title",
    ]
    if any([file.ignore_predicted_filename_differences[f] for f in ignore_flags]):
        return None
    predicted_filename = file.create_filename()
    if file.filename != predicted_filename:
        return analysis(
            errors=MusicFileError(
                "File name differs from expected",
                [
                    MusicFileErrorFix(
                        f"Change file name to expected: {quoted(predicted_filename)}",
                        RenameFileCommand.create(ordinal, predicted_filename),
                    ),
                    MusicFileErrorFix(
                        "Ignore",
                        EditFileCommand.create(
                            ordinal,
                            ignore=[IgnoreFilenameDifferences.CONSISTENT_FILENAME],
                        ),
                    ),
                ],
            )
        )
