from typing import List, Union

from functions.music_file.MusicFileErrorFix import MusicFileErrorFix
from libs.list_union_util import SimpleList, simple_list


class MusicFileError:
    text: str
    fixes: List[MusicFileErrorFix]

    def __init__(
            self, text: str, fixes: SimpleList[MusicFileErrorFix] = None
    ):
        self.text = text
        if fixes:
            self.fixes = simple_list(fixes)
        else:
            self.fixes = []
