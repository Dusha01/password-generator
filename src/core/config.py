from dataclasses import dataclass

from src.core.utils.validate_config import validate_config


@dataclass(frozen=True)
class GeneratorConfig:

    length: int
    lowercase: bool
    uppercase: bool
    digits: bool
    symbols: bool
    no_ambiguous: bool


    def __post_init__(self):
        validate_config(self)


    @classmethod
    def defaults(cls) -> "GeneratorConfig":
        return cls(
            length=16,
            lowercase=True,
            uppercase=True,
            digits=True,
            symbols=True,
            no_ambiguous=False,
        )