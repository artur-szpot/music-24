class MusicFileErrorFix:
    text: str
    command: str
    with_user_input: bool

    def __init__(self, text: str, command: str, with_user_input: bool = False):
        self.text = text
        self.command = command
        self.with_user_input = with_user_input

    @staticmethod
    def with_user_input(text: str, command: str):
        return MusicFileErrorFix(text, command, True)

    @staticmethod
    def boolean_options(index: int, tag: str):
        return [
            MusicFileErrorFix(f"Set to true", f"edit-file {index} --{tag} 1"),
            MusicFileErrorFix(f"Set to false", f"edit-file {index} --{tag} 0"),
        ]

    @staticmethod
    def rating_options(index: int):
        return [
            MusicFileErrorFix(f"Set to {i}", f"edit-file {index} --rating {i}")
            for i in range(1, 11)
        ]
