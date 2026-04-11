from __future__ import annotations

import sys
from collections.abc import Sequence
from importlib.metadata import EntryPoint, entry_points

ENTRY_POINT_GROUP = "pnfl.commands"


def _discover_commands() -> dict[str, EntryPoint]:
    """Return {name: EntryPoint} for every installed pnfl subcommand."""
    return {ep.name: ep for ep in entry_points(group=ENTRY_POINT_GROUP)}


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    commands = _discover_commands()

    if not argv or argv[0] in ("-h", "--help"):
        print_usage(commands)
        return 0

    command = argv[0]
    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        print_usage(commands)
        return 1

    func = commands[command].load()
    return func(argv[1:])


def print_usage(commands: dict[str, EntryPoint]) -> None:
    print("usage: pnfl <command> [args...]\n")
    print("commands:")
    for name in sorted(commands):
        print(f"  {name}")


if __name__ == "__main__":
    raise SystemExit(main())
