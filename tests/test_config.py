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
        cfg.validate()

    def test_validate_length_too_short(self) -> None:
        cfg = GeneratorConfig(2, True, True, True, True, False)
        with pytest.raises(ValueError, match="Length 2 must be at least 4"):
            cfg.validate()

    def test_validate_length_zero(self) -> None:
        cfg = GeneratorConfig(0, True, False, False, False, False)
        with pytest.raises(ValueError, match="at least 1"):
            cfg.validate()

    def test_validate_length_negative(self) -> None:
        cfg = GeneratorConfig(-1, True, True, True, True, False)
        with pytest.raises(ValueError, match="at least 4"):
            cfg.validate()

    def test_validate_length_too_long(self) -> None:
        cfg = GeneratorConfig(257, True, False, False, False, False)
        with pytest.raises(ValueError, match="must not exceed 256"):
            cfg.validate()

    def test_validate_no_categories(self) -> None:
        cfg = GeneratorConfig(16, False, False, False, False, False)
        with pytest.raises(ValueError, match="At least one character category"):
            cfg.validate()
