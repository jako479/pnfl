# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Tracked the rename of two coach subcommand projects: `fbpro98-gameplanreader` → `pnfl-gameplanreader` and `fbpro98-gameplanwriter` → `pnfl-gameplanwriter`. Updated dependency list, build-release shipping list, system-test imports, and `read-gameplan` / `write-gameplan` documentation. The umbrella subcommand names are unchanged.

## [0.1.0] - 2026-05-23

### Added
- Initial umbrella CLI dispatching to PNFL subcommands.
- Subcommand discovery via entry points (replacing hardcoded list).
- System test for `read-gameplan` -> `write-gameplan` pipeline.
- System test for `convert-pdb`.
- Documentation for the scheduler subcommand.
- Locked release PyPI dependencies; proper `__init__.py`.
- `STATUS.md` and `TEST_STATUS.md` documentation; standardized project config and docs.
- Colorized logging via `_logging` module.
- Line-ending rules in `.editorconfig`.

### Changed
- Cleaned up README and clarified example calls in release READMEs.
- Restructured release READMEs with per-tool help/example sections; clarified `install.bat`.
- Renamed `LICENSE.txt` to `LICENSE` for GitHub auto-detection.
- Split admin release orchestration into separate `pnfl-admin` project.
- Standardized project tooling config.

### Fixed
- Release build no longer attempts to copy nonexistent `LICENSE.txt`.
- Gameplan test updates aligned with subcommand changes.
