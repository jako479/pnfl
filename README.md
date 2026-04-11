# pnfl

Umbrella CLI for PNFL tools. Dispatches to subcommands provided by individual packages.

## Setup

```bash
pip install -e ".[dev]"
```

## Usage

```bash
pnfl <command> [args...]
pnfl --help
```

## Tools

### `convert-pdb`

Export a WinLogStats `.pdb` to an Excel workbook. Optionally annotates with one or two offensive and defensive game plans.

Provided by [`pnfl-pdbtoexcel`](../pnfl-pdbtoexcel).

```bash
pnfl convert-pdb --help
pnfl convert-pdb stats.pdb output.xlsm
pnfl convert-pdb stats.pdb output.xlsm -o offense.pln -d defense.pln
pnfl convert-pdb stats.pdb output.xlsm -o offense1.pln -o2 offense2.pln -d defense1.pln -d2 defense2.pln
```

### `read-gameplan`

Extract the play list from a `.pln` game plan file. Outputs to console or text file.

Provided by [`fbpro98-gameplanreader`](../fbpro98-gameplanreader).

```bash
pnfl read-gameplan --help
pnfl read-gameplan offense.pln
pnfl read-gameplan offense.pln --sort name --output plays.txt
```

### `write-gameplan`

Update the 64 normal-play slots of a `.pln` game plan file from a text file of play names.

Provided by [`fbpro98-gameplanwriter`](../fbpro98-gameplanwriter).

```bash
pnfl write-gameplan --help
pnfl write-gameplan offense.pln plays.txt
pnfl write-gameplan offense.pln plays.txt --play-path E:\SIERRA\FbPro98\PNFL
```

### `catalog-plays` _(admin only)_

Build an Excel catalog of every play in a PNFL play tree.

Provided by [`pnfl-playcatalog`](../pnfl-playcatalog).

```bash
pnfl catalog-plays --help
pnfl catalog-plays catalog.xlsm
pnfl catalog-plays catalog.xlsm --play-path E:\SIERRA\FbPro98\PNFL
```

## Build

```bash
py -3.13 scripts/build_release.py
```

Produces two zips in `dist/`:

- **PNFL-v{version}.zip** — coach release
- **PNFL-Admin-v{version}.zip** — admin release (superset of coach)

### Configuring release contents

Edit the lists in `scripts/build_release.py`:

- `COACH_SUBCOMMANDS` — subcommand projects included in both releases
- `SHARED_DEPENDENCY_PROJECTS` — private projects built as wheels for all releases
- `SHARED_PYPI_DEPENDENCIES` — PyPI packages needed by all releases
- `ADMIN_SUBCOMMANDS` — subcommand projects added only to the admin release
- `ADMIN_DEPENDENCY_PROJECTS` — private projects needed only by admin subcommands
- `ADMIN_PYPI_DEPENDENCIES` — PyPI packages needed only by admin subcommands

The CLI auto-discovers available commands at runtime, so no code changes are needed when adding or removing subcommands from a release.

## Testing

```bash
pytest
```

## Installation

End users install via the release zip:

1. Extract `PNFL-v{version}.zip` (or `PNFL-Admin-v{version}.zip`) to a folder.
2. Open a command prompt in that folder.
3. Run `install.bat`.

This installs the bundled wheels into the user's Python environment. After install, `pnfl <command>` is available from any terminal — that is the actual interface to every tool.

Requires Python 3.10 or later with "Add Python to PATH" enabled.

## Uninstallation

```bash
py -m pip uninstall pnfl pnfl-pdbtoexcel pnfl-playcatalog fbpro98-gameplanreader fbpro98-gameplanwriter fbpro98-gameplan fbpro98-play pnfl-playpool
```

Coach releases won't have `pnfl-playcatalog` — pip will warn and skip it.
