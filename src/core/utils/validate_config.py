from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config import GeneratorConfig


def validate_config(config: "GeneratorConfig") -> None:
    min_length = sum([config.lowercase, config.uppercase, config.digits, config.symbols])

    if config.length < min_length:
        raise ValueError(
            f"Length {config.length} must be at least {min_length} "
            f"(number of enabled character categories)"
        )
    
    if config.length < 1:
        raise ValueError("Length must be positive")
    
    if config.length > 256:
        raise ValueError("Length must not exceed 256")
    
    if not any([config.lowercase, config.uppercase, config.digits, config.symbols]):
        raise ValueError("At least one character category must be enabled")