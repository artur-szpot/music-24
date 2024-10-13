def quoted(value: str) -> str:
    escaped = value.replace('"', '"')
    return f'"{escaped}"'


def indefinite(value: str) -> str:
    # Imperfect, but good enough here :)
    article = "an" if value[0] in 'aeiou' else "a"
    return f"{article} {value}"
