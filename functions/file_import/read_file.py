from typing import Optional, List, Dict

from mutagen import File

from functions.data_types.ArtistRole import ArtistRole
from functions.data_types.artist_registry import artist_registry
from functions.file_management.RatingMapper import RatingMapper
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from libs.io import extract_filename_from_path


def tag(value: str) -> Optional[bool]:
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
    artists = {
        str(artist): [ArtistRole.Original]
        for artist in mutagen_file.tags.get("TPE1", [])
    }

    predicted_title, predicted_artists = predicted_artists_and_title(filename[:-4])
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
    filename: str,
) -> [List[str], Dict[str, List[ArtistRole]]]:
    blocks = filename.split(" - ")
    if len(blocks) == 1:
        return [filename, {}]
    title_block = " - ".join(blocks[1:])
    title_blocks = title_block.split(" [")
    if len(title_blocks) == 1:
        original_artists = ""
    elif len(title_blocks) > 2:
        return [
            title_block,
            full_artist_string_to_artists(blocks[0], ArtistRole.Original),
        ]
    else:
        original_artists = title_blocks[1].split("]")[0]
    artists = full_artist_string_to_artists(
        blocks[0], ArtistRole.Remixer if len(original_artists) else ArtistRole.Original
    )
    if len(original_artists):
        artists.update(
            full_artist_string_to_artists(original_artists, ArtistRole.Original)
        )
    return title_blocks[0], artists


def full_artist_string_to_artists(
    value: str, main_role: ArtistRole
) -> Dict[str, List[ArtistRole]]:
    values = value.split(" feat. ")
    artists = half_artist_string_to_artists(values[0], [main_role])
    if len(values) > 1:
        artists.update(
            half_artist_string_to_artists(values[1], [main_role, ArtistRole.Feat])
        )
    return artists


def half_artist_string_to_artists(
    value: str, roles: List[ArtistRole]
) -> Dict[str, List[ArtistRole]]:
    by_comma = value.split(", ")
    last = by_comma[-1]
    if " & " in last and not artist_registry.find(last):
        return {key: roles for key in by_comma[:-1] + last.split(" & ")}
    return {key: roles for key in by_comma}


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
