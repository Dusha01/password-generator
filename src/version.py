"""Версия приложения. Читается из pyproject.toml."""

import re
from pathlib import Path


def _get_version() -> str:
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    text = pyproject.read_text()
    m = re.search(r'version\s*=\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    raise RuntimeError("Version not found in pyproject.toml")


__version__ = _get_version()
