import pytest

from src.core.config import GeneratorConfig


class TestGeneratorConfig:
    def test_defaults(self) -> None:
        cfg = GeneratorConfig.defaults()
        assert cfg.length == 16
        assert cfg.lowercase is True
        assert cfg.uppercase is True
        assert cfg.digits is True
        assert cfg.symbols is True
        assert cfg.no_ambiguous is False

    def test_validate_ok(self) -> None:
        cfg = GeneratorConfig(16, True, True, True, True, False)
        assert cfg.length == 16

    def test_validate_length_too_short(self) -> None:
        with pytest.raises(ValueError, match="Length 2 must be at least 4"):
            GeneratorConfig(2, True, True, True, True, False)

    def test_validate_length_zero(self) -> None:
        with pytest.raises(ValueError, match="at least 1"):
            GeneratorConfig(0, True, False, False, False, False)

    def test_validate_length_negative(self) -> None:
        with pytest.raises(ValueError, match="at least 4"):
            GeneratorConfig(-1, True, True, True, True, False)

    def test_validate_length_too_long(self) -> None:
        with pytest.raises(ValueError, match="must not exceed 256"):
            GeneratorConfig(257, True, False, False, False, False)

    def test_validate_no_categories(self) -> None:
        with pytest.raises(ValueError, match="At least one character category"):
            GeneratorConfig(16, False, False, False, False, False)
