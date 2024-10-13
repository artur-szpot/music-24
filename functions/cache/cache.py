from typing import Optional, List, Union

from functions.cache.CacheContainer import CacheContainer
from functions.execute.ExecutionResult import ExecutionResult
from functions.music_file.MusicFile import MusicFile
from libs.list_union_util import SimpleList, simple_list

cache_container = CacheContainer()
CURRENT_FILE = "current_file"
FILES_TO_IMPORT = "files_to_import"
LAST_QUERY = "last_query"
LAST_RESULT = "last_result"


# COMMAND STACK


def get_next_command() -> Optional[str]:
    command_stack = cache_container.command_stack
    if not len(command_stack):
        return None
    next_command = command_stack[0]
    cache_container.command_stack = command_stack[1:]
    return next_command


def extend_command_stack(commands: SimpleList[str]) -> None:
    cache_container.command_stack.extend(simple_list( commands))


# COMMAND LOG


def get_command_log() -> List[str]:
    return cache_container.command_log


def log_command(command: str) -> None:
    cache_container.command_log = cache_container.command_log[-99:] + [command]


# CURRENT FILE


def set_current_file(file: MusicFile) -> None:
    cache_container.file_cache[CURRENT_FILE] = file


def get_current_file() -> Optional[MusicFile]:
    return cache_container.file_cache.get(CURRENT_FILE)


def clear_current_file() -> None:
    if CURRENT_FILE in cache_container.file_cache:
        del cache_container.file_cache[CURRENT_FILE]


# FILES TO IMPORT


def get_files_to_import() -> Optional[List[MusicFile]]:
    return cache_container.file_cache.get(FILES_TO_IMPORT)


def set_files_to_import(files: List[MusicFile]) -> None:
    cache_container.file_cache[FILES_TO_IMPORT] = files


def clear_files_to_import() -> None:
    if FILES_TO_IMPORT in cache_container.file_cache:
        del cache_container.file_cache[FILES_TO_IMPORT]


def update_files_to_import(file: MusicFile) -> None:
    cache_container.file_cache[FILES_TO_IMPORT][file.get_ordinal_number() - 1] = file


# LAST QUERY


def set_last_query(result: ExecutionResult) -> None:
    cache_container.query_cache[LAST_QUERY] = result


def get_last_query() -> Optional[ExecutionResult]:
    return cache_container.query_cache.get(LAST_QUERY)


# LAST RESULT


def set_last_result(result: ExecutionResult) -> None:
    cache_container.query_cache[LAST_RESULT] = result


def get_last_result() -> Optional[ExecutionResult]:
    return cache_container.query_cache.get(LAST_RESULT)
