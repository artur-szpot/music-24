from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_any_artists_set(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    if not len(file.artists):
        fixes = []
        if file.predicted_artists:
            artists = []
            for artist, roles in file.predicted_artists.items():
                artists.append(quoted(artist))
                for role in roles:
                    artists.append(role.value)
            fixes.append(
                MusicFileErrorFix(
                    f"Add artists based on file name: {', '.join(file.predicted_artists)}",
                    f"edit-file {ordinal} --artists {' '.join(artist for artist in artists)}",
                )
            )
        else:
            fixes.append(
                MusicFileErrorFix(
                    f'Add "unknown" artist',
                    f"edit-file {ordinal} --artists unknown",
                )
            )
        fixes.append(
            MusicFileErrorFix.with_user_input(
                "Add artists...",
                f"edit-file {ordinal} --artists ",
            )
        )
        return analysis(errors=MusicFileError("No artists in tags", fixes))
