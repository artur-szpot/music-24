class CommandEnum:
    Exit = 0  # close the app
    ListFiles = 2  # list the files in the file_management
    View = 3  # set how the list view is presented
    # view lAt = length author(sort by) title
    ImportFiles = 4  # look through the files in the directory set for importing from, add them to file_management and move to proper storage folder
    EditDatabaseFile = 5  # change whatever values for the file in database
    UpdateFromMp3 = 6  # set database values from mp3 file
    UpdateFromDatabase = 7  # set mp3 values from database file
    # query for files with given properties (can give return size, then random)
    # save query results as albums or playlists
    # export query results/albums/playlists in different formats (win, car, ?)
    # save info about what has been exported (i.e. listened to)
    AnalyzeImport = 8  # analyze files before importing them
    # organize files (compile files, dictify artists, genres)
    # create indexes for faster access?
    # continuous command mode (ls -> next; edit -> author)
    # stats
    # set artist/genre alt-names
    # set artist/genre misspellings and use them to correct saved data
    # rewrite artist/genre from one value to another


def get_command_dictionary():
    command_registry = {
        CommandEnum.Exit: ["exit", "x"],
        CommandEnum.ListFiles: ["list-files", "ls"],
        CommandEnum.View: ["view", "v"],
        CommandEnum.ImportFiles: ["import-files", "if"],
        CommandEnum.EditDatabaseFile: ["edit-file", "ef"],
        CommandEnum.AnalyzeImport: ["analyze-import", "ai"],
    }

    command_dictionary = {}

    for command in command_registry:
        for code in command_registry[command]:
            if code in command_dictionary:
                raise KeyError(f"Repeated code {code} detected")
            command_dictionary[code] = command

    return command_dictionary
