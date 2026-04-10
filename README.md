# pnfl

Umbrella CLI for PNFL tools. Dispatches to subcommands provided by individual packages.

## Setup

```bash
pip install -e ".[dev]"
```

## Usage

```bash
pnfl <command> [args...]
```

### Coach commands

| Command          | Package                | Description                        |
| ---------------- | ---------------------- | ---------------------------------- |
| `convert-pdb`    | pnfl-pdbtoexcel        | Export WinLogStats .pdb to Excel   |
| `read-gameplan`  | fbpro98-gameplanreader | Extract plays from .pln files      |
| `write-gameplan` | fbpro98-gameplanwriter | Update .pln files from a play list |

### Admin commands

Admin releases include all coach commands plus:

| Command         | Package          | Description                     |
| --------------- | ---------------- | ------------------------------- |
| `catalog-plays` | pnfl-playcatalog | Build an Excel catalog of plays |

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

This installs the bundled wheels into the user's Python environment. After install, `pnfl <command>` is available from any terminal.

Requires Python 3.10 or later with "Add Python to PATH" enabled.

## Uninstallation

```bash
py -m pip uninstall pnfl pnfl-pdbtoexcel pnfl-playcatalog fbpro98-gameplanreader fbpro98-gameplanwriter fbpro98-gameplan fbpro98-play pnfl-playpool
```

Coach releases won't have `pnfl-playcatalog` — pip will warn and skip it.
