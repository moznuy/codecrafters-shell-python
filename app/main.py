from __future__ import annotations

import os
import subprocess
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


def try_find_executable(path: str) -> str | None:
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
            sys.stderr.write(f"{param} not found\n")
            sys.stderr.flush()
    sys.stdout.flush()


def cmd_pwd(*params):
    sys.stdout.write(os.getcwd() + "\n")
    sys.stdout.flush()


def cmd_cd(*params):
    to = "~"
    if params:
        to = params[0]
    # TODO: too many arguments
    path = os.path.expanduser(to)
    if not os.path.exists(path):
        # TODO: cd: {path}:
        sys.stderr.write(f"{path}: No such file or directory\n")
        sys.stderr.flush()
        return
    os.chdir(path)


COMMAND_MAP = {
    "exit": cmd_exit,
    "echo": cmd_echo,
    "type": cmd_type,
    "pwd": cmd_pwd,
    "cd": cmd_cd,
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
        if fn is not None:
            fn(*params)
            continue

        if executable := try_find_executable(command):
            args = [executable] + params
            handle = subprocess.Popen(args)
            handle.wait()
            continue

        sys.stderr.write(f"{command}: command not found\n")
        sys.stderr.flush()
        continue


if __name__ == "__main__":
    main()
