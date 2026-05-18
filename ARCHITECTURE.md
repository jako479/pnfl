# pnfl — Architecture

Umbrella CLI that dispatches `pnfl <command>` invocations to subcommand packages installed in the same Python environment.

## Module layout

```
src/pnfl/
├── __init__.py    # empty package marker
└── cli.py         # entry-point discovery + dispatch + main()
```

`scripts/build_release.py` builds the zipped coach release. The admin/commissioner releases are built from the private sibling `pnfl-admin` repo.

## What this package does

- Provides the `pnfl` console-script entry point
- Discovers subcommands at runtime via the `pnfl.commands` setuptools entry-point group
- Forwards `argv[1:]` to the loaded subcommand's `main()` and returns its exit code
- Prints a usage listing of every discovered command for `pnfl`, `pnfl --help`, and unknown commands

## What this package assumes

- Each subcommand package exposes a `main(argv: Sequence[str]) -> int` callable, declared under the `pnfl.commands` entry-point group in its `pyproject.toml`
- Subcommands handle their own argparse, I/O, configuration, and exit codes — `pnfl` does not interpret their arguments

## What this package enforces

- Unknown command → exit code 1 with a usage listing to stderr
- No args / `--help` → exit code 0 with usage listing to stdout

## What this package does NOT do

- Parse subcommand arguments
- Load subcommand-specific configuration
- Bundle subcommands directly — installation is via pip wheels (driven by the release script)

## Subcommand discovery

Each subcommand project declares its CLI in its own `pyproject.toml`:

```toml
[project.entry-points."pnfl.commands"]
read-gameplan = "fbpro98_gameplanreader.cli:main"
```

`importlib.metadata.entry_points(group="pnfl.commands")` then surfaces the command at runtime, so adding or removing a subcommand from a release requires no code change here.

Current subcommands: `convert-pdb`, `read-gameplan`, `write-gameplan`, `catalog-plays` (admin), `generate-schedule` (commissioner). The coach release ships only the first three; admin/commissioner releases add the rest.

## Testing

- `tests/test_cli.py` — argparse-style contract for the umbrella (help, unknown command, passthrough)
- `tests/test_gameplan.py` — system-level pipeline tests that wire `read-gameplan` and `write-gameplan` together with copied fixtures in `tests/data/`
- `tests/test_convert_pdb.py` — system test driving `convert-pdb` through the umbrella against a real `.pdb` fixture in `tests/data/`
