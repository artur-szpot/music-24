# from functions.commands.definition.ArgsDict import ArgsDict
# from functions.execute.validate.ArgsValidator import ArgsValidator
# from functions.file_import.read_file import read_file
# from functions.music_file.MusicFile import MusicFileDbProps, MusicFile
# from functions.file_management.file_operations import save_file
#
#
# def update_from_mp3(args_dict: ArgsDict):
#     file = ArgsValidator.get_file(args_dict)
#     return update_from_mp3_exe(file)
#
#
# def update_from_mp3_exe(db_file: MusicFile):
#     music_file = read_file(db_file.path)
#     music_file.db_props = db_file.db_props
#     music_file.set_db_prop(MusicFileDbProps.Desynced, False)
#     save_file(filename, music_file)
#     return ["ok"]
