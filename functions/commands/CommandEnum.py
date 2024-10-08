from enum import Enum


class CommandEnum(Enum):
    Exit = 0  # close the app
    ListFiles = 2  # list the files in the file_management
    FileDetails = 15  # List all the info about a chosen file
    ImportFiles = 4  # look through the files in the directory set for importing from, add them to file_management and move to proper storage folder
    EditDatabaseFile = 5  # change whatever values for the file in database
    UpdateFromMp3 = 6  # set database values from mp3 file
    UpdateFromDatabase = 7  # set mp3 values from database file
    # query for files with given properties (can give return size, then random)
    # save query results as albums or playlists
    # export query results/albums/playlists in different formats (win, car, ?)
    # save info about what has been exported (i.e. listened to)
    AnalyzeImport = 8  # analyze files before importing them
    Fix = 17  # apply auto fixes to found problems
    # organize files (compile files, dictify artists, genres)
    # create indexes for faster access?
    # continuous command mode (ls -> next; edit -> author)
    # stats
    # set artist/genre alt-names
    # set artist/genre misspellings and use them to correct saved data_types
    # rewrite artist/genre from one value to another
    Help = 9

    # Nevigate to certain pages of the iterable result.
    NextPage = 10
    PreviousPage = 11
    SetPageNumber = 12
    SetPageSize = 13

    # Mostly for debug. TODO: Make this safe or remove.
    ClearDatabase = 14

    # How to display stuff
    SetColorScheme = 16
    # View = 3  # set how the list view is presented
    # view lAt = length author(sort by) title
    # ["view", "v"],
