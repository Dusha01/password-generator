import secrets
from typing import TYPE_CHECKING

from .charset import build_charset, get_required_categories


if TYPE_CHECKING:
    from collections.abc import Sequence


def generate(
    length: int,
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    no_ambiguous: bool = False,
) -> str:
    charset = build_charset(
        lowercase=lowercase,
        uppercase=uppercase,
        digits=digits,
        symbols=symbols,
        no_ambiguous=no_ambiguous,
    )

    required = get_required_categories(
        lowercase=lowercase,
        uppercase=uppercase,
        digits=digits,
        symbols=symbols,
        no_ambiguous=no_ambiguous,
    )

    if length < len(required):
        raise ValueError(
            f"Length {length} is less than number of required categories ({len(required)})"
        )

    result: list[str] = list(_shuffle(required))

    remaining = length - len(required)
    for _ in range(remaining):
        result.append(secrets.choice(charset))

    return "".join(_shuffle(result))


def _shuffle(seq: "Sequence[str]") -> list[str]:
    lst = list(seq)
    for i in range(len(lst) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]
    return lst
