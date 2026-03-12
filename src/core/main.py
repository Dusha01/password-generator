"""Точка входа CLI."""

import sys

from src.core.cli import main as cli_main


def main() -> None:
    """Запуск CLI."""
    sys.exit(cli_main())


if __name__ == "__main__":
    main()
