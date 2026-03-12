import string


# Базовые наборы
LOWERCASE: str = string.ascii_lowercase
UPPERCASE: str = string.ascii_uppercase
DIGITS: str = string.digits
SYMBOLS: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Неоднозначные символы (0/O, 1/l/I и т.д.) — исключаются при --no-ambiguous
AMBIGUOUS_CHARS: str = "0O1lI"

# Наборы без неоднозначных символов
LOWERCASE_SAFE: str = "".join(c for c in LOWERCASE if c not in AMBIGUOUS_CHARS)
UPPERCASE_SAFE: str = "".join(c for c in UPPERCASE if c not in AMBIGUOUS_CHARS)
DIGITS_SAFE: str = "".join(c for c in DIGITS if c not in AMBIGUOUS_CHARS)
SYMBOLS_SAFE: str = SYMBOLS


def build_charset(
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    no_ambiguous: bool = False,
) -> str:
    parts: list[str] = []

    if lowercase:
        parts.append(LOWERCASE_SAFE if no_ambiguous else LOWERCASE)
    if uppercase:
        parts.append(UPPERCASE_SAFE if no_ambiguous else UPPERCASE)
    if digits:
        parts.append(DIGITS_SAFE if no_ambiguous else DIGITS)
    if symbols:
        parts.append(SYMBOLS_SAFE if no_ambiguous else SYMBOLS)

    if not parts:
        raise ValueError("At least one character category must be enabled")

    return "".join(parts)


def get_required_categories(
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    no_ambiguous: bool = False,
) -> list[str]:
    result: list[str] = []
    if lowercase:
        result.append((LOWERCASE_SAFE if no_ambiguous else LOWERCASE)[0])
    if uppercase:
        result.append((UPPERCASE_SAFE if no_ambiguous else UPPERCASE)[0])
    if digits:
        result.append((DIGITS_SAFE if no_ambiguous else DIGITS)[0])
    if symbols:
        result.append((SYMBOLS_SAFE if no_ambiguous else SYMBOLS)[0])
    return result
