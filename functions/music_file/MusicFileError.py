from typing import List, Union

from functions.music_file.MusicFileErrorFix import MusicFileErrorFix


class MusicFileError:
    text: str
    fixes: List[MusicFileErrorFix]

    def __init__(
        self, text: str, fixes: Union[MusicFileErrorFix, List[MusicFileErrorFix]] = None
    ):
        self.text = text
        if fixes:
            self.fixes = fixes if isinstance(fixes, list) else [fixes]
        else:
            self.fixes = []
