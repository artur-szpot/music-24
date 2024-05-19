class CommandEnum:
    Exit = 0  # close the app
    CreateTest = 1  # create a test file
    ListFiles = 2  # list the files in the db
    View = 3  # set how the list view is presented
    # view lAt = length author(sort by) title
    ImportFiles = 4  # look through the files in the directory set for importing from, add them to db and move to proper storage folder
    EditFile = 5 # change whatever values for the file

def get_command_dictionary():
    command_registry = {
        CommandEnum.Exit: ['exit', 'x'],
        CommandEnum.CreateTest: ['create-test', 'ct'],
        CommandEnum.ListFiles: ['list-files', 'ls'],
        CommandEnum.View: ['view', 'v'],
        CommandEnum.ImportFiles: ['import-files', 'if'],
        CommandEnum.EditFile: ['edit-file', 'ef'],
    }

    command_dictionary = {}

    for command in command_registry:
        for code in command_registry[command]:
            if code in command_dictionary:
                raise KeyError(f"Repeated code {code} detected")
            command_dictionary[code] = command

    return command_dictionary
