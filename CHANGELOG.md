# Changelog

- Rename `fbpro98-gameplan{reader,writer}` → `pnfl-gameplan{reader,writer}`; subcommand names unchanged.
- Initial umbrella CLI dispatching to PNFL subcommands.
- Subcommand discovery via entry points (replaces hardcoded list).
- System test: `read-gameplan` → `write-gameplan` pipeline.
- System test: `convert-pdb`.
- Scheduler subcommand docs.
- Locked release PyPI deps; proper `__init__.py`.
- `STATUS.md`, `TEST_STATUS.md`, `.editorconfig`.
- Colorized logging via `_logging`.
- README cleanup; per-tool help/example sections in release READMEs; clarified `install.bat`.
- Renamed `LICENSE.txt` → `LICENSE` for GitHub auto-detection.
- Split admin release orchestration into `pnfl-admin`.
- Standardized project tooling config.
- Release build no longer copies nonexistent `LICENSE.txt`.
- Gameplan test updates aligned with subcommand changes.
