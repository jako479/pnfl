"""System test: the convert-pdb subcommand dispatched through the pnfl umbrella."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest

from pnfl.cli import main

TESTS_DIR = Path(__file__).resolve().parent
DATA_DIR = TESTS_DIR / "data"
PDB_PATH = DATA_DIR / "2045-2047.pdb"

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

EXPECTED_SHEETS = ["Options", "Run Plays", "Pass Plays", "Def Plays", "Tendencies"]

# A complete [CategoryOrder] is required: convert-pdb validates that every play
# category is listed before it will build a workbook.
CONVERT_PDB_CONFIG = """\
[Settings]
CalculateTotalStats = Yes
CalculatePercentages = Yes

[CategoryOrder]
RunCategories =
    RL
    RM
    RR
    GLR
PassCategories =
    PSL
    PSM
    PSR
    PML
    PMM
    PMR
    PLR
    PRD
    GLP
DefenseCategories =
    RunLeft
    RunMiddle
    RunRight
    RunDazzle
    PassShort
    PassMedium
    PassLong
    PassDazzle
    GLrun
    GLpass
"""


def _sheet_names(workbook: Path) -> list[str]:
    with ZipFile(workbook) as archive:
        tree = ET.fromstring(archive.read("xl/workbook.xml"))
    return [sheet.attrib["name"] for sheet in tree.findall(f".//{{{MAIN_NS}}}sheet")]


def _write_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "convert-pdb.ini"
    config_path.write_text(CONVERT_PDB_CONFIG, encoding="utf-8")
    return config_path


def test_convert_pdb_via_umbrella_creates_workbook(tmp_path: Path) -> None:
    output = tmp_path / "stats.xlsx"
    config = _write_config(tmp_path)
    exit_code = main(["convert-pdb", str(PDB_PATH), str(output), "--config", str(config)])
    assert exit_code == 0
    assert output.is_file()
    assert _sheet_names(output) == EXPECTED_SHEETS


def test_convert_pdb_rejects_missing_input(tmp_path: Path) -> None:
    output = tmp_path / "stats.xlsx"
    config = _write_config(tmp_path)
    with pytest.raises(SystemExit):
        main(["convert-pdb", str(tmp_path / "missing.pdb"), str(output), "--config", str(config)])
    assert not output.exists()
