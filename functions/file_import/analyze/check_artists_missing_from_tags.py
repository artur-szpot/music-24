from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_artists_missing_from_tags(
    file: MusicFile, ordinal: int
) -> Optional[AnalysisResult]:
    if file.ignore_predicted_filename_differences[
        IgnoreFilenameDifferences.ARTISTS_MISSING_FROM_TAGS
    ]:
        return None
    errors = []
    for artist in file.predicted_artists:
        # alias existing artist to {}
        # replace existing artist
        fixes = []
        if artist not in file.artists:
            errors.append(
                MusicFileError(
                    f"Artist missing from tags: {artist}",
                    [
                        MusicFileErrorFix(
                            "Add artist to tags",
                            f"edit-file {ordinal} --add-artists {quoted(artist)}",
                        ),
                        # todo continue here
                        MusicFileErrorFix(
                            f"Add {artist} as an alias for...",
                            f"edit-file {ordinal} --add-artists {quoted(artist)}",
                        ),
                        MusicFileErrorFix(
                            "Ignore",
                            f"edit-file {ordinal} "
                            f"--ignore {IgnoreFilenameDifferences.CONSISTENT_TITLE.value}",
                        ),
                    ],
                )
            )

        return analysis(errors=errors)
