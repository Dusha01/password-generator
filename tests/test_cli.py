import subprocess
import sys
from pathlib import Path

from src.version import __version__


def _run(args: list[str]) -> subprocess.CompletedProcess:
    project_root = Path(__file__).resolve().parent.parent
    return subprocess.run(
        [sys.executable, "run.py"] + args,
        capture_output=True,
        text=True,
        cwd=project_root,
    )


class TestCLI:
    def test_help(self) -> None:
        r = _run(["--help"])
        assert r.returncode == 0
        assert "pwgen" in r.stdout
        assert "--length" in r.stdout
        assert "--no-digits" in r.stdout

    def test_version(self) -> None:
        r = _run(["--version"])
        assert r.returncode == 0
        assert __version__ in r.stdout

    def test_default_generates_password(self) -> None:
        r = _run(["--length", "16"])
        assert r.returncode == 0
        pw = r.stdout.strip()
        assert len(pw) == 16
        assert len(pw) == len(pw.strip())

    def test_length_option(self) -> None:
        r = _run(["--length", "24"])
        assert r.returncode == 0
        assert len(r.stdout.strip()) == 24

    def test_no_symbols(self) -> None:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        for _ in range(5):
            r = _run(["--length", "32", "--no-symbols"])
            assert r.returncode == 0
            pw = r.stdout.strip()
            assert not any(c in symbols for c in pw)

    def test_invalid_all_categories_disabled(self) -> None:
        r = _run(["--no-digits", "--no-symbols", "--no-uppercase", "--no-lowercase"])
        assert r.returncode == 1
        assert "Error" in r.stderr
        assert "at least one" in r.stderr.lower()

    def test_count_generates_multiple(self) -> None:
        r = _run(["--count", "5", "--length", "8"])
        assert r.returncode == 0
        lines = r.stdout.strip().split("\n")
        assert len(lines) == 5
        assert all(len(pw) == 8 for pw in lines)

    def test_output_to_file(self, tmp_path: Path) -> None:
        out_file = tmp_path / "passwords.txt"
        r = _run(["--count", "2", "--output", str(out_file)])
        assert r.returncode == 0
        content = out_file.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 2

    def test_passphrase_mode(self) -> None:
        r = _run(["--passphrase"])
        assert r.returncode == 0
        pw = r.stdout.strip()
        words = pw.split("-")
        assert len(words) == 4

    def test_passphrase_custom_words(self) -> None:
        r = _run(["--passphrase", "--words", "6"])
        assert r.returncode == 0
        words = r.stdout.strip().split("-")
        assert len(words) == 6
