import subprocess
import sys


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "run.py"] + args,
        capture_output=True,
        text=True,
        cwd="/home/dusha/Projects/CLI/password-generator",
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
        assert "0.1.0" in r.stdout

    def test_default_generates_password(self) -> None:
        r = _run([])
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
