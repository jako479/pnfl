# pnfl — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- Umbrella CLI contract: help and no-args usage, unknown-command rejection, discovered-command listing, and argument passthrough to subcommands
- `read-gameplan` / `write-gameplan` cross-CLI pipelines, including file-based and stdin/stdout round trips for normal and special plays against gold fixtures
- `convert-pdb` dispatched through the umbrella against a real `.pdb` fixture, including workbook structure and missing-input rejection

## Needs tests

- Nothing outstanding for the current scope.
