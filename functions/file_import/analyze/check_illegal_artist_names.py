from typing import Optional

from functions.data_types.Artist import Artist
from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_illegal_artist_names(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    errors = []
    for artist in file.artists:
        corrected_artist = Artist.check_legal_name(artist)
        if corrected_artist is None:
            continue
        errors.append(
            MusicFileError(
                f"Artist with illegal symbols in their name: {artist}",
                [
                    MusicFileErrorFix(
                        f"Change artist name to {corrected_artist}",
                        f"edit-file {ordinal} --remove-artists {quoted(artist)} "
                        f"--add-artists {quoted(corrected_artist)}",
                    ),
                    MusicFileErrorFix.with_user_input(
                        f"Change artist name to...",
                        f"edit-file {ordinal} --remove-artists {quoted(artist)} --add-artists ",
                    ),
                ],
            )
        )
    return analysis(errors=errors)
