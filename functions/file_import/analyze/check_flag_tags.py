from typing import Optional

from functions.file_import.analyze.analysis_helpers import AnalysisResult, analysis
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileErrorFix import MusicFileErrorFix


def check_flag_tags(file: MusicFile, ordinal: int) -> Optional[AnalysisResult]:
    errors = []

    if file.is_dad is None:
        errors.append(
            MusicFileError(
                "Dad flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_dad"),
            )
        )

    if file.is_mlp is None:
        errors.append(
            MusicFileError(
                "MLP flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_mlp"),
            )
        )

    if file.is_ready is None:
        errors.append(
            MusicFileError(
                "Ready flag not set",
                MusicFileErrorFix.boolean_options(ordinal, "is_ready"),
            )
        )

    return analysis(errors=errors)
