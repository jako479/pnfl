from __future__ import annotations

from unittest.mock import patch

from pnfl.cli import main


def test_help_exits_zero(capsys):
    assert main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "pnfl <command>" in output


def test_no_args_shows_help(capsys):
    assert main([]) == 0
    output = capsys.readouterr().out
    assert "pnfl <command>" in output


def test_unknown_command_exits_one(capsys):
    assert main(["bogus"]) == 1
    output = capsys.readouterr().err
    assert "Unknown command: bogus" in output


def test_available_commands_shown_in_help(capsys):
    main(["--help"])
    output = capsys.readouterr().out
    assert "read-gameplan" in output
    assert "write-gameplan" in output


def test_subcommand_passthrough():
    """Verify a subcommand receives the forwarded args."""
    called_with = []

    def fake_main(argv):
        called_with.extend(argv)
        return 0

    with patch("pnfl.cli.import_module") as mock_import:
        mock_import.return_value.main = fake_main
        result = main(["read-gameplan", "foo.pln", "--sort", "name"])

    assert result == 0
    assert called_with == ["foo.pln", "--sort", "name"]
