# pnfl — Status

**Status: Complete**

Umbrella CLI for PNFL tools that dispatches `pnfl <command>` invocations to subcommand packages installed in the same Python environment.

## Implemented

- `pnfl` console-script entry point with runtime subcommand discovery via the `pnfl.commands` entry-point group
- Argument passthrough to each subcommand's `main()` with exit-code forwarding
- Usage listing for `pnfl`, `pnfl --help`, and unknown commands, with unknown commands exiting non-zero
- Five wired subcommands: `convert-pdb`, `read-gameplan`, `write-gameplan`, `catalog-plays` (admin), `generate-schedule` (commissioner)
- Coach release build script producing the distributable zip, with configurable subcommand and dependency lists and a pinned third-party requirements manifest

## Remaining

- Nothing outstanding for the current scope.
