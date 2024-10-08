from functions.lines.Line import Line
from functions.music_file.MusicFile import MusicFile


def file_view_header(file: MusicFile) -> Line:
    return Line.key_value("File name", file.filename)
