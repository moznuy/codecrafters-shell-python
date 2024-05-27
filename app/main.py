import sys


def cmd_exit(*params):
    exit_code = 0
    if params:
        exit_code = int(params[0])
    sys.exit(exit_code)


def echo(*params):
    sys.stdout.write(" ".join(params))
    sys.stdout.write("\n")
    sys.stdout.flush()


COMMAND_MAP = {
    "exit": cmd_exit,
    "echo": echo,
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
