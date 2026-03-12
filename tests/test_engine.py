import string

import pytest

from src.modules.generator.charset import build_charset
from src.modules.generator.engine import generate


class TestGenerate:
    def test_length_matches(self) -> None:
        for length in (8, 16, 24, 32):
            pw = generate(length)
            assert len(pw) == length

    def test_all_chars_from_charset(self) -> None:
        charset = set(build_charset())
        pw = generate(32)
        assert all(c in charset for c in pw)

    def test_contains_lowercase_when_enabled(self) -> None:
        pw = generate(16, lowercase=True, uppercase=False, digits=False, symbols=False)
        assert any(c in string.ascii_lowercase for c in pw)
        assert pw.islower()

    def test_contains_uppercase_when_enabled(self) -> None:
        pw = generate(16, lowercase=False, uppercase=True, digits=False, symbols=False)
        assert any(c in string.ascii_uppercase for c in pw)
        assert pw.isupper()

    def test_contains_digits_when_enabled(self) -> None:
        pw = generate(16, lowercase=False, uppercase=False, digits=True, symbols=False)
        assert any(c in string.digits for c in pw)
        assert pw.isdigit()

    def test_contains_symbols_when_enabled(self) -> None:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pw = generate(16, lowercase=False, uppercase=False, digits=False, symbols=True)
        assert any(c in symbols for c in pw)

    def test_no_ambiguous_excludes_ambiguous(self) -> None:
        ambiguous = "0O1lI"
        for _ in range(20):
            pw = generate(16, no_ambiguous=True)
            assert not any(c in ambiguous for c in pw)

    def test_different_passwords_each_call(self) -> None:
        passwords = {generate(16) for _ in range(100)}
        assert len(passwords) == 100

    def test_length_less_than_categories_raises(self) -> None:
        with pytest.raises(ValueError, match="Length 2 is less than number of required"):
            generate(2, lowercase=True, uppercase=True, digits=True, symbols=True)

    def test_length_equals_categories_ok(self) -> None:
        pw = generate(4, lowercase=True, uppercase=True, digits=True, symbols=True)
        assert len(pw) == 4

    @pytest.mark.parametrize("length", [0, -1])
    def test_invalid_length_raises(self, length: int) -> None:
        with pytest.raises(ValueError):
            generate(length)
