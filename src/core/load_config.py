import json
from pathlib import Path
from typing import Any

# Корень проекта (где лежит src/) — для pipx/editable install
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _get_config_paths() -> list[Path]:
    """Пути к конфигу (порядок: проект → cwd → домашняя директория)."""
    return [
        _PROJECT_ROOT / ".config" / "pwgen" / "config.json",
        _PROJECT_ROOT / ".pwgenrc",
        Path.cwd() / ".config" / "pwgen" / "config.json",
        Path.cwd() / ".pwgenrc",
        Path.home() / ".config" / "pwgen" / "config.json",
        Path.home() / ".pwgenrc",
    ]


def load_config_file() -> dict[str, Any] | None:
    for path in _get_config_paths():
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
    return None


def merge_with_cli(config: dict[str, Any] | None, cli_args: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if config:
        result.update(config)

    for key, value in cli_args.items():
        if value is not None:
            result[key] = value

    return result
