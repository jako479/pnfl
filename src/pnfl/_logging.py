"""Shared logging configuration for the `pnfl` umbrella CLI.

Configures the root logger with a colorized StreamHandler so every `pnfl
<command>` invocation gets red ERROR / yellow WARNING output on stderr.
Honors the `NO_COLOR` environment variable per https://no-color.org and
auto-disables color when stderr is not a TTY (so piped output stays clean).

This module is `pnfl`-internal; subcommand packages should not import it.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import ClassVar


class _ColorFormatter(logging.Formatter):
    """Wraps formatted messages in ANSI color codes based on level."""

    _COLORS: ClassVar[dict[int, str]] = {
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[1;31m",  # bold red
    }
    _RESET: ClassVar[str] = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        color = self._COLORS.get(record.levelno)
        if color and self._color_enabled():
            return f"{color}{msg}{self._RESET}"
        return msg

    @staticmethod
    def _color_enabled() -> bool:
        if os.environ.get("NO_COLOR"):
            return False
        return sys.stderr.isatty()


def configure_logging(level: int = logging.INFO) -> None:
    """Attach a colorized StreamHandler to the root logger, once.

    No-ops if the root logger already has handlers — so a subcommand's own
    `logging.basicConfig(...)` falls through when the umbrella has already
    configured logging, and a direct subcommand invocation (without the
    umbrella) still gets vanilla logging from that fallback `basicConfig`.
    """
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(_ColorFormatter("%(levelname)s: %(message)s"))
    root.addHandler(handler)
    root.setLevel(level)
