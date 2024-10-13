from typing import List, Tuple, Optional

from functions.music_file.MusicFileError import MusicFileError
from libs.list_union_util import SimpleList, simple_list

AnalysisResult = Tuple[List[MusicFileError], List[MusicFileError]]


def analysis(
        errors: SimpleList[MusicFileError] = None,
        warnings: SimpleList[MusicFileError] = None) -> Optional[
    AnalysisResult]:
    return simple_list(errors), simple_list(warnings)
