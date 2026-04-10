from __future__ import annotations

import sys
from collections.abc import Sequence
from importlib import import_module

ALL_COMMANDS = [
    ("catalog-plays", "pnfl_playcatalog.cli"),
    ("convert-pdb", "pnfl_pdbtoexcel.cli"),
    ("read-gameplan", "fbpro98_gameplanreader.cli"),
    ("write-gameplan", "fbpro98_gameplanwriter.cli"),
]

COMMANDS: dict[str, str] = {}
for _name, _module in ALL_COMMANDS:
    try:
        import_module(_module)
        COMMANDS[_name] = _module
    except ImportError:
        pass


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print_usage()
        return 0

    command = argv[0]
    if command not in COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        print_usage()
        return 1

    module = import_module(COMMANDS[command])
    return module.main(argv[1:])


def print_usage() -> None:
    print("usage: pnfl <command> [args...]\n")
    print("commands:")
    for name in COMMANDS:
        print(f"  {name}")


if __name__ == "__main__":
    raise SystemExit(main())
