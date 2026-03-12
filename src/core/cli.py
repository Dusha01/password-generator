import argparse
import sys

from src.core.config import GeneratorConfig
from src.modules.generator import generate
from src.version import __version__


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pwgen",
        description="CLI utility for generating cryptographically secure passwords.",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=16,
        metavar="N",
        help="Password length (default: 16).",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits.",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude special symbols.",
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters.",
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters.",
    )
    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="Exclude ambiguous characters (0/O, 1/l/I).",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    config = GeneratorConfig(
        length=args.length,
        lowercase=not args.no_lowercase,
        uppercase=not args.no_uppercase,
        digits=not args.no_digits,
        symbols=not args.no_symbols,
        no_ambiguous=args.no_ambiguous,
    )
    try:
        config.validate()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    password = generate(
        length=config.length,
        lowercase=config.lowercase,
        uppercase=config.uppercase,
        digits=config.digits,
        symbols=config.symbols,
        no_ambiguous=config.no_ambiguous,
    )
    print(password)
    return 0


def main() -> int:
    parser = _create_parser()
    args = parser.parse_args()
    return run(args)