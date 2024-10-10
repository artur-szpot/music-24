from typing import Optional, List

from mutagen import File

from functions.data_types.artist_registry import artist_registry
from functions.music_file.MusicFile import MusicFile
from functions.file_management.RatingMapper import RatingMapper
from functions.music_file.MusicFileError import MusicFileError
from libs.io import extract_filename_from_path


def tag(value: str) -> bool:
    if value is None:
        return value
    else:
        try:
            return bool(int(str(value)))
        except:
            return False


def read_file(path: str) -> MusicFile:
    filename = extract_filename_from_path(path)
    if not path.lower().endswith(".mp3"):
        return MusicFile(
            {
                "path": path,
                "filename": filename,
                "errors": [MusicFileError("File in a wrong format")],
            }
        )
    mutagen_file = File(path)
    rating_tag = mutagen_file.tags.get("POPM:no@email")
    artists = [str(artist) for artist in mutagen_file.tags.get("TPE1", [])]
    predicted_title, predicted_artists = predicted_artists_and_title(
        filename[:-4], artists
    )
    music_file = MusicFile(
        {
            "artists": artists,
            "genres": [str(artist) for artist in mutagen_file.tags.get("TCON", [])],
            "title": str(mutagen_file.tags.get("TIT2", "")),
            "path": path,
            "db_file": None,
            "filename": filename,
            "length": int(mutagen_file.info.length),
            "rating": RatingMapper.from_mp3_tags(
                -1 if rating_tag is None else int(rating_tag.rating)
            ),
            "is_mlp": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom3:XXX")),
            "is_dad": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom2:XXX")),
            "is_ready": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom1:XXX")),
            "predicted_title": predicted_title or "",
            "predicted_artists": predicted_artists or [],
        }
    )
    return music_file


def predicted_artists_and_title(
    filename: str, ampersand_artists: Optional[List[str]] = None
) -> [List[str], Optional[str]]:
    blocks = filename.split(" - ")
    if len(blocks) == 1:
        return [None, []]
    artists = artists_from_string(blocks[0], ampersand_artists)
    title_block = " - ".join(blocks[1:])
    title_blocks = title_block.split(" [")
    if len(title_blocks) == 1:
        return [title_block, artists]
    if len(title_blocks) > 2:
        return [None, artists]
    original_artists = artists_from_string(
        title_blocks[1].split("]")[0], ampersand_artists
    )
    return title_blocks[0], artists + original_artists


def artists_from_string(
    value: str, ampersand_artists: Optional[List[str]] = None
) -> List[str]:
    comma_split = value.split(", ")
    if len(comma_split) == 1:
        return [value]
    ampersand_split = comma_split[-1].split(" & ")
    if len(ampersand_split) == 1:
        return comma_split
    feat_split = ampersand_split[-1].split(" feat. ")
    if len(feat_split) == 1:
        return comma_split[:-1] + ampersand_split
    return (
        comma_split[:-1]
        + reconnect_ampersand_artists(ampersand_split[:-1], ampersand_artists)
        + [feat_split[0]]
        + artists_from_string(feat_split[1])
    )


def reconnect_ampersand_artists(
    artists: List[str], ampersand_artists: Optional[List[str]] = None
) -> List[str]:
    return_artists = []
    skip = False
    for index in range(len(artists)):
        if skip:
            skip = False
            continue
        if index < len(artists) - 1:
            potential_artist = f"{artists[index]} & {artists[index + 1]}"
            if (
                artist_registry.find(potential_artist)
                or potential_artist in ampersand_artists
            ):
                return_artists.append(potential_artist)
                skip = True
            else:
                return_artists.append(artists[index])
    return return_artists
