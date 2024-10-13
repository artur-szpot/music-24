from typing import Optional

from functions.data_types.Artist import Artist
from functions.data_types.artist_registry import artist_registry
from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.strings import quoted


def check_new_artists(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    warnings = []
    for artist in file.artists:
        corrected_artist = Artist.check_legal_name(artist)
        if corrected_artist is not None:
            continue
        if artist_registry.find(artist):
            continue
        warnings.extend(
            [
                MusicFileError(
                    f"New artist: {artist}",
                    [
                        MusicFileErrorFix(
                            f"Add new artist",
                            f"add-artist {quoted(artist)}",
                        ),
                    ],
                ),
                MusicFileErrorFix.with_user_input(
                    f"Add as alias...",
                    f"add-artist-alias {quoted(artist)} ",
                ),
                MusicFileErrorFix.with_user_input(
                    f"Add as misspelling...",
                    f"add-artist-misspelling {quoted(artist)} ",
                ),
            ]
        )
    return analysis(warnings=warnings)
