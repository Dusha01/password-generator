import sys
from pathlib import Path

from src.i18n import t


def write_to_stdout(passwords: list[str]) -> None:
    for pw in passwords:
        print(pw)


def write_to_file(
    passwords: list[str],
    path: Path | str,
    *,
    warn_if_world_readable: bool = True,
) -> None:
    filepath = Path(path)
    filepath.write_text("\n".join(passwords) + "\n", encoding="utf-8")

    if warn_if_world_readable and filepath.exists():
        mode = filepath.stat().st_mode
        if mode & 0o004:
            print(t("warning_file_readable", path=str(filepath)), file=sys.stderr)


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
    except ImportError:
        return False

    pyperclip.copy(text)
    return True