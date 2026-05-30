"""System tests: cross-CLI pipelines between read-gameplan and write-gameplan."""

from __future__ import annotations

import io
import shutil
from pathlib import Path

import pytest
from fbpro98_gameplan import CustomPlay, read_gameplan
from pnfl_gameplanreader.cli import main as read_main
from pnfl_gameplanwriter.cli import main as write_main

TESTS_DIR = Path(__file__).resolve().parent
DATA_DIR = TESTS_DIR / "data"
EXPECTED_DIR = DATA_DIR / "expected"
PLAYPOOL_DIR = DATA_DIR / "plays"
TEMPLATE_PLN = DATA_DIR / "O_64_06a.pln"
GOLD_PLN = EXPECTED_DIR / "O_64_06a.pln"
SEEDED_AF_KO_PLN = DATA_DIR / "seeded_specials_af_ko.pln"

# Pinned values for SEEDED_AF_KO_PLN: TEMPLATE_PLN's custom normals with
# AF-KO as the only custom special (AF-KO.ply is the only special-teams
# play in the test playpool).
EXPECTED_AF_KO_NORMALS: list[str] = [
    "or45rl01",
    "or10rlrg",
    "sf35hevy",
    "ne25rls1",
    "tt10draw",
    "db57rrlt",
    "sf68swp1",
    "at21draw",
    "or68rmtr",
    "sf28ore3",
    "mn24ct11",
    "dc14rm02",
    "orx8rmt2",
    "dn28rmx3",
    "kc27swp3",
    "jj41rodr",
    "mn21ctr",
    "dn28rm01",
    "jj1aarrx",
    "af1awagr",
    "jj1adrgx",
    "af1ain2t",
    "kc1xhoth",
    "sf1aslnt",
    "ps1hwagr",
    "kc2bmnr1",
    "lv2z2out",
    "lv2afloc",
    "lac2yspd",
    "kc2aslot",
    "gpa2zfax",
    "sf3uzipt",
    "dn3ysr01",
    "dn3x4got",
    "ne3ybblt",
    "gpa3xfaz",
    "wa7yafly",
    "at7awgrt",
    "lv4xzzip",
    "at4aqp01",
    "kc4zqukb",
    "at4acrsb",
    "la4xwhdg",
    "gpa5xcoy",
    "atf5zcsb",
    "sf5xmima",
    "sf8bstop",
    "gp5xtop1",
    "at8zrold",
    "atf6zrgs",
    "sf6arolr",
    "or6z01r",
    "jj66xhot",
    "kc6spidr",
    "at9axcrx",
    "or91flyx",
    "az9zcutl",
    "ny9hwhlr",
    "atgzslot",
    "atfgslot",
    "gbgpx03",
    "ny0zflyz",
    "or0hsnap",
    "atf0lobt",
]
EXPECTED_AF_KO_SPECIALS: list[str | None] = [None, "af-ko", None, None, None, None, None, None, None, None]


def _custom_normal_names(pln: Path) -> list[str]:
    gp = read_gameplan(pln)
    return [p.name.casefold() for p in gp.normal_plays if isinstance(p, CustomPlay)]


def _custom_special_names(pln: Path) -> list[str | None]:
    gp = read_gameplan(pln)
    return [(p.name.casefold() if p is not None else None) for p in gp.custom_special_plays]


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
    """Reader extracts specials from the seeded PLN; writer applies them; specials match pinned values, normals untouched."""
    spec_txt = tmp_path / "spec.txt"
    assert read_main([str(SEEDED_AF_KO_PLN), "--special-out", str(spec_txt)]) == 0

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

    assert _custom_special_names(target_pln) == EXPECTED_AF_KO_SPECIALS
    assert _custom_normal_names(target_pln) == pre_normals


def test_gameplan_round_trip_combined_files(tmp_path: Path) -> None:
    """Reader extracts normals+specials from the seeded PLN; writer applies them; both match pinned values."""
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    assert (
        read_main(
            [
                str(SEEDED_AF_KO_PLN),
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

    assert _custom_normal_names(target_pln) == EXPECTED_AF_KO_NORMALS
    assert _custom_special_names(target_pln) == EXPECTED_AF_KO_SPECIALS


# ---------- stdin/stdout round trip ----------


def test_gameplan_round_trip_combined_stdin(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reader emits 64+10 headerless lines; writer reads the 74-line combined stream from stdin."""
    assert read_main([str(SEEDED_AF_KO_PLN), "--normal-out", "-", "--special-out", "-"]) == 0
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

    assert _custom_normal_names(target_pln) == EXPECTED_AF_KO_NORMALS
    assert _custom_special_names(target_pln) == EXPECTED_AF_KO_SPECIALS


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
    assert read_main([str(SEEDED_AF_KO_PLN), "--special-out", "-"]) == 0
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

    assert _custom_special_names(target_pln) == EXPECTED_AF_KO_SPECIALS
    assert _custom_normal_names(target_pln) == pre_normals
