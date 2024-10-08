from mutagen import File
from mutagen.id3 import TPE1, TCON, TIT2, POPM, COMM

from functions.execute.ArgsValidator import ArgsValidator
from functions.music_file.MusicFile import MusicFileDbProps, MusicFile
from functions.file_management.RatingMapper import RatingMapper
from functions.file_management.file_operations import save_file


def update_from_database(args_dict):
    file = ArgsValidator.get_file(args_dict)
    return update_from_database_exe(file)


def update_from_database_exe(db_file: MusicFile):
    mutagen_file = File(db_file.path)
    mutagen_file.tags["TPE1"] = TPE1(encoding=3, text=db_file.authors)
    mutagen_file.tags["TCON"] = TCON(encoding=3, text=db_file.genres)
    mutagen_file.tags["TIT2"] = TIT2(encoding=3, text=db_file.title)
    mutagen_file.tags["POPM:no@email"] = POPM(
        email="no@email", rating=RatingMapper.to_mp3_tags(db_file.rating)
    )
    mutagen_file.tags["POPM:no@email"] = COMM(
        encoding=3,
        lang="XXX",
        desc="Songs-DB_Custom3",
        text=[str(int(db_file.is_mlp))],
    )
    mutagen_file.tags["POPM:no@email"] = COMM(
        encoding=3,
        lang="XXX",
        desc="Songs-DB_Custom2",
        text=[str(int(db_file.is_dad))],
    )
    mutagen_file.tags["POPM:no@email"] = COMM(
        encoding=3,
        lang="XXX",
        desc="Songs-DB_Custom1",
        text=[str(int(db_file.is_ready))],
    )
    mutagen_file.save()
    db_file.set_db_prop(MusicFileDbProps.Desynced, False)
    save_file(db_file.filename, db_file)
    return ["ok"]
