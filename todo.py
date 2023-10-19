#!/usr/bin/env python3
"""Find all `@todo` comments in the `.` and `src` directories"""
from dataclasses import dataclass
from enum import Enum
from os import getenv, listdir, path, walk
from sys import platform
from typing import List

if platform == "win32":
    from os import system

    system("")


class Style(Enum):
    RESET = "\u001b[0m"
    BOLD = "\u001b[1m"
    ITALICIZE = "\u001b[3m"
    UNDERLINE = "\u001b[4m"


@dataclass
class ToDo:
    filepath: str
    message: str

    def __repr__(self) -> str:
        return f"{Style.BOLD.value}{self.message}{Style.RESET.value}\nIn: {Style.UNDERLINE.value}{self.filepath}{Style.RESET.value}"


def get_filepaths() -> List[str]:
    filepaths = [
        path.join(".", f)
        for f in listdir(".")
        if path.isfile(f) and f.split(".")[-1] in ["js", "ejs", "ts"]
    ]
    for root, dirnames, filenames in walk("src"):
        for filename in filenames:
            filepaths.append(path.join(root, filename))
    return filepaths


def get_todos() -> List[ToDo]:
    todos = []
    for filepath in get_filepaths():
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()
            todo_start = 0
            for i in range(0, len(lines)):
                if "@todo" in lines[i]:
                    todo_start = i + 1
                    message = ""
                    while "//" in lines[i]:
                        message = f"{message}\n{lines[i].strip()}"
                        i += 1
                    message = (
                        message.strip()
                        .strip("\n")
                        .replace("//", "")
                        .strip()
                        .removeprefix("@todo:")
                        .removeprefix("@todo")
                        .strip()
                    )
                    if message != "":
                        _message = list(message)
                        _message[0] = _message[0].upper()
                        todos.append(
                            ToDo(
                                filepath=f"{filepath}:{todo_start}",
                                message="".join(_message),
                            )
                        )
                    else:
                        todos.append(
                            ToDo(
                                filepath=f"{filepath}:{todo_start}",
                                message=f"Line {todo_start}",
                            )
                        )
                todo_start = 0
    return todos


if __name__ == "__main__":
    todos = get_todos()
    if len(todos) > 0:
        for todo in todos:
            print(f"{todo}\n")
    else:
        print(
            f"{Style.BOLD.value}No {Style.RESET.value}{Style.ITALICIZE.value if (str(getenv('TERM_PROGRAM')) != 'vscode' or getenv('TERM') is not None) else Style.BOLD.value}`@todo`{Style.RESET.value}{Style.BOLD.value}(s) found.{Style.RESET.value}"
        )
