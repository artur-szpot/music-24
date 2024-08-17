from functions.definition.ArgsDict import ArgsDict
from functions.execute.ArgsValidator import ArgsValidator
from functions.file_import.read_file import read_file
from functions.file_management.MusicFile import MusicFileDbProps
from functions.file_management.file_operations import open_file, save_file


def update_from_mp3(args_dict: ArgsDict):
    filename = ArgsValidator.get_filename(args_dict)
    return update_from_mp3_exe(filename)


def update_from_mp3_exe(filename):
    db_file = open_file(filename)
    music_file = read_file(db_file.path)
    music_file.db_props = db_file.db_props
    music_file.set_db_prop(MusicFileDbProps.Desynced, False)
    save_file(filename, music_file)
    return ["ok"]
