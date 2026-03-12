import secrets

from .wordlist import WORDS


def generate_passphrase(
    words_count: int = 4,
    *,
    separator: str = "-",
) -> str:
    if words_count < 1:
        raise ValueError("words_count must be at least 1")
    if words_count > 20:
        raise ValueError("words_count must not exceed 20")

    words = [secrets.choice(WORDS) for _ in range(words_count)]
    return separator.join(words)
