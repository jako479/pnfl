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

### `generate-schedule` _(commissioner only)_

Generate a PNFL season schedule with OR-Tools.

Provided by [`pnfl-scheduler`](../pnfl-scheduler).

```bash
pnfl generate-schedule --help
pnfl generate-schedule --output season.html --season 2026
pnfl generate-schedule --output season.html --season 2026 --scheduler two-phase-rank
```

## Build

```bash
py -3.13 scripts/build_release.py
```

Produces **PNFL-v{version}.zip** in `dist/` — the coach release. Admin and commissioner releases are built from the private `pnfl-admin` orchestration repo (sibling of this one) and are not produced by this script.

### Configuring release contents

Edit the lists in `scripts/build_release.py`:

- `COACH_SUBCOMMANDS` — subcommand projects shipped in the coach release
- `SHARED_DEPENDENCY_PROJECTS` — private library projects built as wheels for the release

The CLI auto-discovers available commands at runtime, so no code changes are needed when adding or removing subcommands from a release.

### Third-party PyPI dependencies (`release-requirements.txt`)

This file is a pinned-version manifest of every third-party PyPI package shipped in the release zip. The build script feeds it to `pip download`, which resolves transitive dependencies automatically and downloads every required wheel into the release `packages/` folder.

Format is standard pip requirements syntax:

```
xlsxwriter==3.2.9
```

Rules:

- **Only list top-level deps.** Transitive deps (what xlsxwriter itself depends on) are pulled automatically — do not list them.
- **Pin exact versions** (`==`) for reproducible builds. Without a pin, every release rebuild could grab a different version.
- **Add a line** when a subcommand gains a new third-party dep. To bump a pin, install the new version locally and update the version number here.

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
