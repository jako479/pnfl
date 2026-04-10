"""Build release zips for the PNFL CLI.

Produces two distributions:
  - PNFL-v{version}.zip        (coach release: read-gameplan, write-gameplan)
  - PNFL-Admin-v{version}.zip  (admin release: adds catalog-plays)

Run from the pnfl project root:
    py -3.13 scripts/build_release.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PNFL_ROOT = PROJECT_ROOT.parent

# Private dependency projects (wheels built for all releases).
SHARED_DEPENDENCY_PROJECTS = [
    PNFL_ROOT / "fbpro98-play",
    PNFL_ROOT / "fbpro98-gameplan",
    PNFL_ROOT / "pnfl-playpool",
]

# Subcommand projects included in each release.
COACH_SUBCOMMANDS = [
    PNFL_ROOT / "fbpro98-gameplanreader",
    PNFL_ROOT / "fbpro98-gameplanwriter",
    PNFL_ROOT / "pnfl-pdbtoexcel",
]

ADMIN_SUBCOMMANDS = [
    PNFL_ROOT / "pnfl-playcatalog",
]

# Private dependency projects only needed in the admin release.
ADMIN_DEPENDENCY_PROJECTS: list[Path] = []

# PyPI dependencies needed by all releases.
SHARED_PYPI_DEPENDENCIES: list[str] = ["xlsxwriter"]

# PyPI dependencies only needed in the admin release.
ADMIN_PYPI_DEPENDENCIES: list[str] = []


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
            sys.executable, "-m", "pip", "wheel",
            "--no-deps", "--wheel-dir", str(output_dir), str(project_dir),
        ],
        check=True,
    )


def download_pypi_deps(packages: list[str], output_dir: Path) -> None:
    """Download PyPI packages as wheels into the output directory."""
    for package in packages:
        print(f"  Downloading: {package}")
        subprocess.run(
            [
                sys.executable, "-m", "pip", "download",
                "--no-deps", "-d", str(output_dir), package,
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


def stage_release(
    release_name: str,
    dist_dir: Path,
    subcommand_projects: list[Path],
    extra_dependency_projects: list[Path],
    pypi_deps: list[str],
    readme_variant: str,
) -> Path:
    """Stage a release folder and return its path."""
    staging = dist_dir / release_name
    packages_dir = staging / "packages"

    if staging.exists():
        shutil.rmtree(staging)
    packages_dir.mkdir(parents=True)

    # Build shared dependency wheels.
    for project in SHARED_DEPENDENCY_PROJECTS + extra_dependency_projects:
        build_wheel(project, packages_dir)

    # Build subcommand wheels.
    for project in subcommand_projects:
        build_wheel(project, packages_dir)

    # Build the pnfl umbrella wheel (provides the `pnfl` console script).
    build_wheel(PROJECT_ROOT, packages_dir)

    # Download PyPI dependencies.
    all_pypi = SHARED_PYPI_DEPENDENCIES + pypi_deps
    if all_pypi:
        download_pypi_deps(all_pypi, packages_dir)

    # Harvest each subproject's user-facing release artifacts (.bat, .ini).
    # Source code is shipped as wheels in packages/, not copied — pip installs
    # everything via install.bat, which generates the `pnfl` console script.
    for project in subcommand_projects:
        copy_subproject_release_artifacts(project, staging)

    # Copy umbrella release files (install.bat, README.txt).
    # README.coach.txt / README.admin.txt are variant-specific — only the
    # selected one is copied, and it lands as plain README.txt in the zip.
    release_dir = PROJECT_ROOT / "release"
    if release_dir.is_dir():
        for release_file in release_dir.glob("*"):
            if not release_file.is_file():
                continue
            if release_file.name.startswith("README.") and release_file.name.endswith(".txt"):
                continue
            shutil.copy2(release_file, staging)
        readme_src = release_dir / f"README.{readme_variant}.txt"
        shutil.copy2(readme_src, staging / "README.txt")

    # License.
    license_src = PROJECT_ROOT / "LICENSE.txt"
    if license_src.exists():
        shutil.copy2(license_src, staging)

    return staging


def main() -> None:
    version = get_version()
    dist_dir = PROJECT_ROOT / "dist"

    # Coach release.
    print("Building coach release...")
    coach_name = f"PNFL-v{version}"
    stage_release(coach_name, dist_dir, COACH_SUBCOMMANDS, [], [], readme_variant="coach")
    shutil.make_archive(str(dist_dir / coach_name), "zip", dist_dir, coach_name)
    print(f"  -> {dist_dir / coach_name}.zip\n")

    # Admin release.
    print("Building admin release...")
    admin_name = f"PNFL-Admin-v{version}"
    stage_release(
        admin_name,
        dist_dir,
        COACH_SUBCOMMANDS + ADMIN_SUBCOMMANDS,
        ADMIN_DEPENDENCY_PROJECTS,
        ADMIN_PYPI_DEPENDENCIES,
        readme_variant="admin",
    )
    shutil.make_archive(str(dist_dir / admin_name), "zip", dist_dir, admin_name)
    print(f"  -> {dist_dir / admin_name}.zip\n")

    print("Done.")


if __name__ == "__main__":
    main()
