"""Версия приложения. Читается из pyproject.toml."""

import re
import sys
from pathlib import Path


def _get_version() -> str:
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent
    pyproject = base / "pyproject.toml"
    text = pyproject.read_text()
    m = re.search(r'version\s*=\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    raise RuntimeError("Version not found in pyproject.toml")


__version__ = _get_version()
