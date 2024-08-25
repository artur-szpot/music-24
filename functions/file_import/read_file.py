from mutagen import File

from functions.file_management.MusicFile import MusicFile
from functions.file_management.RatingMapper import RatingMapper


def read_file(path: str) -> MusicFile:
    if not path.endswith(".mp3"):
        return MusicFile({"path": path, "errors": ["File in a wrong format"]})
    mutagen_file = File(path)
    tag = lambda value: None if value is None else bool(int(str(value)))
    rating_tag = mutagen_file.tags.get("POPM:no@email")
    music_file = MusicFile(
        {
            "authors": [str(author) for author in mutagen_file.tags.get("TPE1", [])],
            "genres": [str(author) for author in mutagen_file.tags.get("TCON", [])],
            "title": str(mutagen_file.tags.get("TIT2", "")),
            "path": path,
            "length": int(mutagen_file.info.length),
            "rating": RatingMapper.from_mp3_tags(
                -1 if rating_tag is None else int(rating_tag.rating)
            ),
            "is_mlp": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom3:XXX")),
            "is_dad": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom2:XXX")),
            "is_ready": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom1:XXX")),
        }
    )
    return music_file
