from typing import Any


def error_message_to_string(message: Any) -> str:
    message = str(message)
    if message[0] == message[-1] and message[0] in ["'", '"']:
        return message[1:-1]
    return message
