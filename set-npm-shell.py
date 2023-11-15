import re
import subprocess
from os import path
from sys import platform

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
        shell_path = shell_path.replace('\\', "\\\\")
        cmd: [str] = ["npm", "config", "set", f'script-shell="{shell_path}"']
        print(cmd)
        subprocess.run(cmd, shell=True)
