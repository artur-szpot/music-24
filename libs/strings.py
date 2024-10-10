def quoted(value: str) -> str:
    escaped = value.replace('"', '"')
    return f'"{escaped}"'
