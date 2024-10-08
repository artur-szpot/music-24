from typing import Optional, List

from mutagen import File

from functions.data_types.author_registry import author_registry
from functions.music_file.MusicFile import MusicFile
from functions.file_management.RatingMapper import RatingMapper
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
    if not path.lower().endswith(".mp3"):
        return MusicFile({"path": path, "errors": ["File in a wrong format"]})
    filename = extract_filename_from_path(path)
    mutagen_file = File(path)
    rating_tag = mutagen_file.tags.get("POPM:no@email")
    authors = [str(author) for author in mutagen_file.tags.get("TPE1", [])]
    predicted_title, predicted_authors = predicted_authors_and_title(
        filename[:-4], authors
    )
    music_file = MusicFile(
        {
            "authors": authors,
            "genres": [str(author) for author in mutagen_file.tags.get("TCON", [])],
            "title": str(mutagen_file.tags.get("TIT2", "")),
            "path": path,
            "filename": filename,
            "length": int(mutagen_file.info.length),
            "rating": RatingMapper.from_mp3_tags(
                -1 if rating_tag is None else int(rating_tag.rating)
            ),
            "is_mlp": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom3:XXX")),
            "is_dad": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom2:XXX")),
            "is_ready": tag(mutagen_file.tags.get("COMM:Songs-DB_Custom1:XXX")),
            "predicted_title": predicted_title or "",
            "predicted_authors": predicted_authors or [],
        }
    )
    return music_file


def predicted_authors_and_title(
    filename: str, ampersand_authors: Optional[List[str]] = None
) -> [List[str], Optional[str]]:
    blocks = filename.split(" - ")
    if len(blocks) == 1:
        return [None, []]
    authors = authors_from_string(blocks[0], ampersand_authors)
    title_block = " - ".join(blocks[1:])
    title_blocks = title_block.split(" [")
    if len(title_blocks) == 1:
        return [title_block, authors]
    if len(title_blocks) > 2:
        return [None, authors]
    original_authors = authors_from_string(
        title_blocks[1].split("]")[0], ampersand_authors
    )
    return title_blocks[0], authors + original_authors


def authors_from_string(
    value: str, ampersand_authors: Optional[List[str]] = None
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
        + reconnect_ampersand_authors(ampersand_split[:-1], ampersand_authors)
        + [feat_split[0]]
        + authors_from_string(feat_split[1])
    )


def reconnect_ampersand_authors(
    authors: List[str], ampersand_authors: Optional[List[str]] = None
) -> List[str]:
    return_authors = []
    skip = False
    for index in range(len(authors)):
        if skip:
            skip = False
            continue
        if index < len(authors) - 1:
            potential_author = f"{authors[index]} & {authors[index + 1]}"
            if (
                author_registry.find_author(potential_author)
                or potential_author in ampersand_authors
            ):
                return_authors.append(potential_author)
                skip = True
            else:
                return_authors.append(authors[index])
    return return_authors
