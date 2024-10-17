from functions.lines.Line import Line
from functions.lines.LineElement import LineElement
from functions.music_file.MusicFile import MusicFile
from functions.settings.text_color.SchemeColor import SchemeColor


def file_view_header(file: MusicFile) -> Line:
    error_count = len(file.errors)
    warning_count = len(file.warnings)
    error_message = []
    if error_count:
        error_message.append(f"{error_count}E")
    if warning_count:
        error_message.append(f"{warning_count}W")
    return Line(
        elements=[
            LineElement.bold("File name "),
            LineElement(file.filename + " "),
            LineElement.bold(
                "OK" if not error_message else ", ".join(error_message),
                SchemeColor.GOOD if not error_message else SchemeColor.BAD,
            ),
        ],
    )
