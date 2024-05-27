import sys


COMMAND_MAP = {}


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


if __name__ == "__main__":
    main()
