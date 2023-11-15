import re
import subprocess
from os import linesep, path
from sys import platform
from typing import List

DEFAULT_PATH = "C:\\Program Files\\Git\\"
DEFAULT_POWERSHELL_PATH = (
    "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
)
CMD_PATH = "C:\\Windows\\System32\\cmd.exe"


def get_git_path() -> str | None:
    result: subprocess.CompletedProcess[bytes] = subprocess.run(
        ["where", "git"], shell=True, capture_output=True
    )
    if result.returncode == 0:
        path_match: re.Match[str] | None = re.match(
            r"^[A-Z]:\\.*\\(?!git\.exe$)", result.stdout.decode()
        )
        if path_match is not None:
            return path_match[0].removesuffix(
                f"{path.basename(path.dirname(path_match[0]))}\\"
            )
    else:
        if path.exists(DEFAULT_PATH):
            return DEFAULT_PATH
    return None


def get_pwsh_path() -> str:
    result: subprocess.CompletedProcess[bytes] = subprocess.run(
        ["where", "pwsh"], shell=True, capture_output=True
    )
    if result.returncode == 0:
        path_match: re.Match[str] | None = re.match(
            r"^[A-Z]:\\.*\\(?!pwsh\.exe$)", result.stdout.decode()
        )
        if path_match is not None:
            return path_match[0]
    else:
        if path.exists(DEFAULT_POWERSHELL_PATH):
            return DEFAULT_POWERSHELL_PATH
    return CMD_PATH


def write_npmrc(npmrc_path: str, lines: List[str]) -> bool:
    file_lines: List[str]
    if not path.exists(npmrc_path):
        with open(npmrc_path, "w", encoding="utf8") as file:
            for line in lines:
                file.write(f"{line}{linesep}")
        with open(npmrc_path, "r", encoding="utf8") as file:
            lines.extend([""])
            file_lines = [line.strip() for line in file.readlines()]
            if file_lines == lines:
                return True
    else:
        with open(npmrc_path, "r", encoding="utf8") as file:
            file_lines = [file_line.strip() for file_line in file.readlines()]
        with open(npmrc_path, "a", encoding="utf8") as file:
            for line in lines:
                if line not in file_lines:
                    file.write(f"{line}{linesep}")
        are_set: int = 0
        with open(npmrc_path, "r", encoding="utf8") as file:
            file_lines = [file_line.strip() for file_line in file.readlines()]
            for line in lines:
                if line in file_lines:
                    are_set += 1
        if are_set == len(lines):
            return True
    return False


if __name__ == "__main__":
    if platform != "win32":
        print("This script is only needed on Windows.")
        exit(0)
    else:
        git_path: str | None = get_git_path()
        shell_path: str = (
            path.join(git_path, "bin", "sh.exe")
            if git_path is not None
            else get_pwsh_path()
        )
        print(f"Shell:\t{shell_path}")
        shell_path = shell_path.replace("\\", "\\\\")
        print(
            "Done!"
            if write_npmrc(
                npmrc_path=path.join(".", ".npmrc"),
                lines=[f'script-shell="{shell_path}"'],
            )
            else "ERROR: Could not set 'script-shell' in '.npmrc'."
        )
