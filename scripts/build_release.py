"""Build the coach release zip for PNFL.

Produces:
  - PNFL-v{version}.zip  (coach release)

Run from the pnfl project root:

    py -3.13 scripts/build_release.py

This script is the coach-release builder only. The admin release is built
from the private ``pnfl-admin`` orchestration repo, which lives as a
sibling of this one. This script has no knowledge of any private admin
subcommand and can be cloned and run stand-alone against the public
sibling repos.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PNFL_ROOT = PROJECT_ROOT.parent

# Shared dependency projects (wheels built and shipped in the release).
SHARED_DEPENDENCY_PROJECTS = [
    PNFL_ROOT / "fbpro98-play",
    PNFL_ROOT / "fbpro98-gameplan",
    PNFL_ROOT / "pnfl-playpool",
]

# Coach subcommand projects shipped in the release.
COACH_SUBCOMMANDS = [
    PNFL_ROOT / "fbpro98-gameplanreader",
    PNFL_ROOT / "fbpro98-gameplanwriter",
    PNFL_ROOT / "pnfl-pdbtoexcel",
]

# Pinned third-party PyPI packages shipped in the release. Transitive deps
# resolved automatically by pip; only top-level entries need to be listed.
RELEASE_REQUIREMENTS = PROJECT_ROOT / "release-requirements.txt"


def get_version() -> str:
    """Read the version from pyproject.toml."""
    pyproject = PROJECT_ROOT / "pyproject.toml"
    match = re.search(r'^version\s*=\s*"(.+?)"', pyproject.read_text(), re.MULTILINE)
    if not match:
        raise RuntimeError("Could not find version in pyproject.toml")
    return match.group(1)


def build_wheel(project_dir: Path, output_dir: Path) -> None:
    """Build a wheel for a project into the output directory."""
    print(f"  Building wheel: {project_dir.name}")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--wheel-dir",
            str(output_dir),
            str(project_dir),
        ],
        check=True,
    )


def download_pypi_deps(requirements_file: Path, output_dir: Path) -> None:
    """Download wheels for every PyPI package in the requirements file (with transitive deps)."""
    print(f"  Downloading from: {requirements_file.name}")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-r",
            str(requirements_file),
            "-d",
            str(output_dir),
        ],
        check=True,
    )


def copy_subproject_release_artifacts(project_dir: Path, staging: Path) -> None:
    """Copy a subproject's user-facing release files into the staging folder.

    Harvests <project>/release/*.bat (launcher templates) and
    <project>/config/*.ini (release configs, skipping *.dev.ini).
    """
    release_dir = project_dir / "release"
    if release_dir.is_dir():
        for bat in release_dir.glob("*.bat"):
            print(f"  Copying launcher: {bat.name}")
            shutil.copy2(bat, staging)

    config_dir = project_dir / "config"
    if config_dir.is_dir():
        for ini in config_dir.glob("*.ini"):
            if ini.name.endswith(".dev.ini"):
                continue
            print(f"  Copying config: {ini.name}")
            shutil.copy2(ini, staging)


def stage_release(release_name: str, dist_dir: Path) -> Path:
    """Stage the coach release folder and return its path."""
    staging = dist_dir / release_name
    packages_dir = staging / "packages"

    if staging.exists():
        shutil.rmtree(staging)
    packages_dir.mkdir(parents=True)

    # Build shared dependency wheels.
    for project in SHARED_DEPENDENCY_PROJECTS:
        build_wheel(project, packages_dir)

    # Build subcommand wheels.
    for project in COACH_SUBCOMMANDS:
        build_wheel(project, packages_dir)

    # Build the pnfl umbrella wheel (provides the `pnfl` console script).
    build_wheel(PROJECT_ROOT, packages_dir)

    # Download PyPI dependencies (root + transitive) from the pinned lock file.
    if RELEASE_REQUIREMENTS.is_file():
        download_pypi_deps(RELEASE_REQUIREMENTS, packages_dir)

    # Harvest each subproject's user-facing release artifacts (.bat, .ini).
    for project in COACH_SUBCOMMANDS:
        copy_subproject_release_artifacts(project, staging)

    # Copy umbrella release files (install.bat, README.txt).
    release_dir = PROJECT_ROOT / "release"
    if release_dir.is_dir():
        for release_file in release_dir.glob("*"):
            if release_file.is_file():
                shutil.copy2(release_file, staging)

    # License.
    license_src = PROJECT_ROOT / "LICENSE.txt"
    if license_src.is_file():
        shutil.copy2(license_src, staging)

    return staging


def main() -> None:
    version = get_version()
    dist_dir = PROJECT_ROOT / "dist"

    print("Building coach release...")
    coach_name = f"PNFL-v{version}"
    stage_release(coach_name, dist_dir)
    shutil.make_archive(str(dist_dir / coach_name), "zip", dist_dir, coach_name)
    print(f"  -> {dist_dir / coach_name}.zip\n")

    print("Done.")


if __name__ == "__main__":
    main()
