from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError


def check_artists_missing_from_filename(
    file: MusicFile, ordinal: int
) -> Optional[AnalysisResult]:
    if file.ignore_predicted_filename_differences[
        IgnoreFilenameDifferences.ARTISTS_MISSING_FROM_FILENAME
    ]:
        return None
    errors = []
    for artist in file.artists:
        if artist not in file.predicted_artists:
            errors.append(MusicFileError(f"Artist missing from file name: {artist}"))
        # alias existing artist to {}
        # replace existing artist
        # todo command to change file name
        # todo command to alias artists

    return analysis(errors=errors)
