import tempfile
from pathlib import Path

import pytest

from src.modules.output import write_to_file, write_to_stdout


class TestWriteToStdout:
    def test_single_password(self, capsys: pytest.CaptureFixture[str]) -> None:
        write_to_stdout(["abc123"])
        captured = capsys.readouterr()
        assert captured.out == "abc123\n"

    def test_multiple_passwords(self, capsys: pytest.CaptureFixture[str]) -> None:
        write_to_stdout(["pw1", "pw2", "pw3"])
        captured = capsys.readouterr()
        assert captured.out == "pw1\npw2\npw3\n"


class TestWriteToFile:
    def test_writes_passwords(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            path = f.name
        try:
            write_to_file(["secret1", "secret2"], path, warn_if_world_readable=False)
            content = Path(path).read_text()
            assert content == "secret1\nsecret2\n"
        finally:
            Path(path).unlink(missing_ok=True)

    def test_path_object(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            path = Path(f.name)
        try:
            write_to_file(["x"], path, warn_if_world_readable=False)
            assert path.read_text() == "x\n"
        finally:
            path.unlink(missing_ok=True)
