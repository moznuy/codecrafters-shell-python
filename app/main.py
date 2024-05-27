from __future__ import annotations

import os
import sys


def cmd_exit(*params):
    exit_code = 0
    if params:
        exit_code = int(params[0])
    sys.exit(exit_code)


def cmd_echo(*params):
    sys.stdout.write(" ".join(params))
    sys.stdout.write("\n")
    sys.stdout.flush()


def try_find_executable(path: os.PathLike) -> str | None:
    env_path = os.environ.get("PATH", "")
    env_path_list = env_path.split(os.pathsep)
    for check_path in env_path_list:
        check_exec = os.path.join(check_path, path)
        if os.path.isfile(check_exec):
            return check_exec
    return None


def cmd_type(*params):
    for param in params:
        if param in COMMAND_MAP:
            sys.stdout.write(f"{param} is a shell builtin\n")
        elif executable := try_find_executable(param):
            sys.stdout.write(f"{param} is {executable}\n")
        else:
            sys.stdout.write(f"{param} not found\n")
    sys.stdout.flush()


COMMAND_MAP = {
    "exit": cmd_exit,
    "echo": cmd_echo,
    "type": cmd_type,
}


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        cmd = input().strip().split()
        if not cmd:
            continue

        command, params = cmd[0], cmd[1:]
        fn = COMMAND_MAP.get(command)
        if fn is None:
            sys.stderr.write(f"{command}: command not found\n")
            sys.stderr.flush()
            continue
        fn(*params)


if __name__ == "__main__":
    main()
