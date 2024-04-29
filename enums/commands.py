class CommandEnum:
    Exit = 0
    CreateTest = 1


CommandDictionary = {
    'exit': CommandEnum.Exit,
    'x': CommandEnum.Exit,
    'create-test': CommandEnum.CreateTest,
    'ct': CommandEnum.CreateTest,
}
