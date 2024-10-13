from enum import Enum


class CommandEnum(Enum):
    Exit = 0  # close the app
    ShowLog = 36

    ListFiles = 2  # list the files in the file_management
    FileDetails = 15  # List all the info about a chosen file
    EditDatabaseFile = 5  # change whatever values for the file in database
    UpdateFromMp3 = 6  # set database values from mp3 file
    UpdateFromDatabase = 7  # set mp3 values from database file
    # query for files with given properties (can give return size, then random)
    # save query results as albums or playlists
    # export query results/albums/playlists in different formats (win, car, ?)
    # save info about what has been exported (i.e. listened to)

    # file import process
    AnalyzeImport = 8  # analyze files before importing them
    Fix = 17  # apply auto fixes to found problems
    # look through the files in the directory set for importing from, add them to file_management and move to proper
    # storage folder
    ImportFiles = 4
    RenameImport = 37  # change the file name to correctly reflect its tags

    # work with data types - artist
    ListArtists = 34
    AddArtist = 18
    RenameArtist = 19  # mostly to change default capitalization
    AddArtistAlias = 20
    # because there should be an artist under this alias, or it became unused
    RemoveArtistAlias = 21
    PromoteArtistAlias = 22
    AddArtistMisspelling = 23
    RemoveArtistMisspelling = 24  # because there should be an artist under this alias
    PromoteArtistMisspelling = 25  # aka make it an alias

    # work with data types - genre
    ListGenres = 35
    AddGenre = 26
    RenameGenre = 27
    AddGenreAlias = 28
    # because there should be a genre under this alias, or it became unused
    RemoveGenreAlias = 29
    PromoteGenreAlias = 30
    AddGenreMisspelling = 31
    RemoveGenreMisspelling = 32  # because there should be a genre under this alias
    PromoteGenreMisspelling = 33  # aka make it an alias

    # organize files (compile files, dictify artists, genres)
    # create indexes for faster access?
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
    # view lAt = length artist(sort by) title
    # ["view", "v"],
