import pytest

from src.modules.generator.charset import (
    AMBIGUOUS_CHARS,
    build_charset,
    DIGITS,
    DIGITS_SAFE,
    LOWERCASE,
    LOWERCASE_SAFE,
    UPPERCASE,
    UPPERCASE_SAFE,
)


class TestBuildCharset:
    def test_default_includes_all_categories(self) -> None:
        cs = build_charset()
        assert any(c in LOWERCASE for c in cs)
        assert any(c in UPPERCASE for c in cs)
        assert any(c in DIGITS for c in cs)
        assert "!" in cs or "@" in cs

    def test_lowercase_only(self) -> None:
        cs = build_charset(lowercase=True, uppercase=False, digits=False, symbols=False)
        assert cs == LOWERCASE

    def test_uppercase_only(self) -> None:
        cs = build_charset(lowercase=False, uppercase=True, digits=False, symbols=False)
        assert cs == UPPERCASE

    def test_digits_only(self) -> None:
        cs = build_charset(lowercase=False, uppercase=False, digits=True, symbols=False)
        assert cs == DIGITS

    def test_symbols_only(self) -> None:
        cs = build_charset(lowercase=False, uppercase=False, digits=False, symbols=True)
        assert "!" in cs and "@" in cs

    def test_no_ambiguous_excludes_ambiguous_chars(self) -> None:
        cs = build_charset(no_ambiguous=True)
        for char in AMBIGUOUS_CHARS:
            assert char not in cs

    def test_no_ambiguous_lowercase(self) -> None:
        cs = build_charset(lowercase=True, uppercase=False, digits=False, symbols=False, no_ambiguous=True)
        assert cs == LOWERCASE_SAFE
        assert "l" not in cs

    def test_no_ambiguous_digits(self) -> None:
        cs = build_charset(lowercase=False, uppercase=False, digits=True, symbols=False, no_ambiguous=True)
        assert cs == DIGITS_SAFE
        assert "0" not in cs and "1" not in cs

    def test_all_disabled_raises(self) -> None:
        with pytest.raises(ValueError, match="At least one character category"):
            build_charset(lowercase=False, uppercase=False, digits=False, symbols=False)
