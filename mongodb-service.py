#!/usr/bin/env python3
import ctypes

is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

import argparse
import subprocess as sp
import sys
from dataclasses import dataclass
from os import makedirs, path

SERVICE_NAME = "MongoDB"
DB_PATH = "C:\\mongodb\\db"
LOG_PATH = "C:\\mongodb\\log.txt"


@dataclass
class CliArgs:
    install: bool
    remove: bool
    start: bool
    stop: bool


def get_args() -> CliArgs:
    parser = argparse.ArgumentParser()
    if "-h" in sys.argv or "--help" in sys.argv:
        parser._print_message(
            f"{path.basename(__file__)}\n\nSERVICE_NAME:\t{SERVICE_NAME}\nDB_PATH:\t{DB_PATH}\nLOG_PATH:\t{LOG_PATH}\n\n"
        )
    action = parser.add_argument_group("Action").add_mutually_exclusive_group(
        required=True
    )
    action.add_argument(
        "--install",
        dest="install",
        action="store_true",
        default=False,
        help=f"install a service for {SERVICE_NAME}",
    )
    action.add_argument(
        "--remove",
        dest="remove",
        action="store_true",
        default=False,
        help=f"remove {SERVICE_NAME} service",
    )
    action.add_argument(
        "--start",
        dest="start",
        action="store_true",
        default=False,
        help=f"start {SERVICE_NAME} service",
    )
    action.add_argument(
        "--stop",
        dest="stop",
        action="store_true",
        default=False,
        help=f"stop {SERVICE_NAME} service",
    )
    return CliArgs(**vars(parser.parse_args()))


def run_as_admin(argv=None):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    else:
        arguments = argv
    argument_line = " ".join(arguments)
    executable = sys.executable
    ret = shell32.ShellExecuteW(None, "runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


def run():
    args = get_args()
    if is_admin:
        if args.install:
            if not path.isdir(DB_PATH):
                makedirs(DB_PATH)

            result = sp.run(
                [
                    "mongod",
                    f"--dbpath={DB_PATH}",
                    f"--logpath={LOG_PATH}",
                    "--install",
                ],
                shell=True,
            )

            print(
                f"Service {SERVICE_NAME} installed"
            ) if result.returncode == 0 else exit(result.returncode)
        elif args.remove:
            result = sp.run(
                ["mongod", "--remove"],
                shell=True,
            )
            print(
                f"Service {SERVICE_NAME} removed"
            ) if result.returncode == 0 else exit(result.returncode)
        else:
            cmd = ["net"]
            if args.start:
                cmd.append("start")
            elif args.stop:
                cmd.append("stop")
            cmd.append(SERVICE_NAME)
            sp.run(cmd, shell=True)
    else:
        run_as_admin(sys.argv)


if __name__ == "__main__":
    run()
