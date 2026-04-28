"""System tests: cross-CLI pipelines."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from fbpro98_gameplan import CustomPlay, read_gameplan
from fbpro98_gameplanreader.cli import main as read_main
from fbpro98_gameplanwriter.cli import main as write_main


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
WRITER_FIXTURES = WORKSPACE_ROOT / "fbpro98-gameplanwriter" / "tests" / "fixtures"
TEMPLATE_PLN = WRITER_FIXTURES / "offense" / "DEN-OGP1.pln"
GOLD_PLN = WRITER_FIXTURES / "offense" / "expected" / "DEN-OGP1.pln"
PLAYPOOL_DIR = WRITER_FIXTURES / "plays"


def _require(path: Path) -> Path:
    if not path.exists():
        pytest.skip(f"Missing sibling fixture: {path}")
    return path


def test_read_then_write_roundtrip(tmp_path: Path) -> None:
    """Read a known-clean gameplan with the reader CLI, write it back with the writer CLI,
    verify the play set survives the trip."""
    gold = _require(GOLD_PLN)
    template = _require(TEMPLATE_PLN)
    pool = _require(PLAYPOOL_DIR)

    plays_txt = tmp_path / "plays.txt"
    assert read_main([str(gold), "--output", str(plays_txt)]) == 0

    target_pln = tmp_path / "DEN-OGP1.pln"
    shutil.copy2(template, target_pln)
    assert write_main([str(target_pln), str(plays_txt), "--play-path", str(pool)]) == 0

    original = read_gameplan(gold)
    reloaded = read_gameplan(target_pln)

    orig_names = [p.name.casefold() for p in original.normal_plays if isinstance(p, CustomPlay)]
    new_names = [p.name.casefold() for p in reloaded.normal_plays if isinstance(p, CustomPlay)]
    assert orig_names == new_names
