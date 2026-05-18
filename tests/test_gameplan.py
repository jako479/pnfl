"""System tests: cross-CLI pipelines between read-gameplan and write-gameplan."""

from __future__ import annotations

import io
import shutil
from pathlib import Path

import pytest
from fbpro98_gameplan import CustomPlay, read_gameplan
from fbpro98_gameplanreader.cli import main as read_main
from fbpro98_gameplanwriter.cli import main as write_main

TESTS_DIR = Path(__file__).resolve().parent
DATA_DIR = TESTS_DIR / "data"
EXPECTED_DIR = DATA_DIR / "expected"
PLAYPOOL_DIR = DATA_DIR / "plays"
TEMPLATE_PLN = DATA_DIR / "O_64_06a.pln"
GOLD_PLN = EXPECTED_DIR / "O_64_06a.pln"

# AF-KO.ply (special_category=2 = Kickoff) is the only special-teams play in
# the test playpool, so round-trip tests for specials must source from a PLN
# that uses only that play.


def _custom_normal_names(pln: Path) -> list[str]:
    gp = read_gameplan(pln)
    return [p.name.casefold() for p in gp.normal_plays if isinstance(p, CustomPlay)]


def _custom_special_names(pln: Path) -> list[str | None]:
    gp = read_gameplan(pln)
    return [(p.name.casefold() if p is not None else None) for p in gp.custom_special_plays]


def _seed_special_source(tmp_path: Path) -> Path:
    """Build a source PLN whose only custom special is AF-KO (slot 2 = Kickoff)."""
    src = tmp_path / "seed.pln"
    shutil.copy2(TEMPLATE_PLN, src)
    spec_txt = tmp_path / "_seed_spec.txt"
    spec_txt.write_text("AF-KO\n", encoding="utf-8")
    assert (
        write_main(
            [
                str(src),
                "--special-plays",
                str(spec_txt),
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )
    return src


# ---------- file-based round trip ----------


def test_gameplan_round_trip_normal_file(tmp_path: Path) -> None:
    """Reader writes normals to a file; writer applies them back; bytes match the gold fixture."""
    plays_txt = tmp_path / "plays.txt"
    assert read_main([str(GOLD_PLN), "--normal-out", str(plays_txt)]) == 0

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)
    assert (
        write_main(
            [
                str(target_pln),
                "--normal-plays",
                str(plays_txt),
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert target_pln.read_bytes() == GOLD_PLN.read_bytes()


def test_gameplan_round_trip_special_file(tmp_path: Path) -> None:
    """Reader extracts specials from a seeded PLN; writer applies them back; specials survive, normals untouched."""
    source = _seed_special_source(tmp_path)
    expected_specials = _custom_special_names(source)

    spec_txt = tmp_path / "spec.txt"
    assert read_main([str(source), "--special-out", str(spec_txt)]) == 0

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)
    pre_normals = _custom_normal_names(target_pln)
    assert (
        write_main(
            [
                str(target_pln),
                "--special-plays",
                str(spec_txt),
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert _custom_special_names(target_pln) == expected_specials
    assert _custom_normal_names(target_pln) == pre_normals


def test_gameplan_round_trip_combined_files(tmp_path: Path) -> None:
    # Compose source: gold's normals, AF-KO as the only special.
    source = tmp_path / "source.pln"
    shutil.copy(GOLD_PLN, source)
    source.chmod(0o644)
    spec_seed = tmp_path / "_seed_spec.txt"
    spec_seed.write_text("AF-KO\n", encoding="utf-8")
    assert (
        write_main(
            [
                str(source),
                "--special-plays",
                str(spec_seed),
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )
    expected_normals = _custom_normal_names(source)
    expected_specials = _custom_special_names(source)

    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    assert (
        read_main(
            [
                str(source),
                "--normal-out",
                str(n_path),
                "--special-out",
                str(s_path),
            ]
        )
        == 0
    )

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)
    assert (
        write_main(
            [
                str(target_pln),
                "--normal-plays",
                str(n_path),
                "--special-plays",
                str(s_path),
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert _custom_normal_names(target_pln) == expected_normals
    assert _custom_special_names(target_pln) == expected_specials


# ---------- stdin/stdout round trip ----------


def test_gameplan_round_trip_combined_stdin(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reader emits 64+10 headerless lines; writer reads the 74-line combined stream from stdin."""
    source = _seed_special_source(tmp_path)
    expected_normals = _custom_normal_names(source)
    expected_specials = _custom_special_names(source)

    assert read_main([str(source), "--normal-out", "-", "--special-out", "-"]) == 0
    captured = capsys.readouterr().out
    assert "===" not in captured  # headerless
    assert len(captured.splitlines()) == 74

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)

    monkeypatch.setattr("sys.stdin", io.StringIO(captured))
    assert (
        write_main(
            [
                str(target_pln),
                "--normal-plays",
                "-",
                "--special-plays",
                "-",
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert _custom_normal_names(target_pln) == expected_normals
    assert _custom_special_names(target_pln) == expected_specials


def test_gameplan_round_trip_normal_stdin(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reader emits headerless normal-only via `--normal-out -`, writer consumes from stdin; bytes match gold fixture."""
    assert read_main([str(GOLD_PLN), "--normal-out", "-"]) == 0
    captured = capsys.readouterr().out
    assert "===" not in captured  # headerless

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)

    monkeypatch.setattr("sys.stdin", io.StringIO(captured))
    assert (
        write_main(
            [
                str(target_pln),
                "--normal-plays",
                "-",
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert target_pln.read_bytes() == GOLD_PLN.read_bytes()


def test_gameplan_round_trip_special_stdin(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reader emits headerless special-only via `--special-out -`, writer consumes from stdin."""
    source = _seed_special_source(tmp_path)
    expected_specials = _custom_special_names(source)

    assert read_main([str(source), "--special-out", "-"]) == 0
    captured = capsys.readouterr().out
    assert "===" not in captured  # headerless
    assert len(captured.splitlines()) == 10

    target_pln = tmp_path / "target.pln"
    shutil.copy2(TEMPLATE_PLN, target_pln)
    pre_normals = _custom_normal_names(target_pln)

    monkeypatch.setattr("sys.stdin", io.StringIO(captured))
    assert (
        write_main(
            [
                str(target_pln),
                "--special-plays",
                "-",
                "--play-path",
                str(PLAYPOOL_DIR),
            ]
        )
        == 0
    )

    assert _custom_special_names(target_pln) == expected_specials
    assert _custom_normal_names(target_pln) == pre_normals
