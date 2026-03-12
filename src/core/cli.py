import argparse
import sys

from src.core.config import GeneratorConfig
from src.core.load_config import load_config_file, merge_with_cli
from src.i18n import set_locale, t
from src.modules.generator import generate, generate_passphrase
from src.modules.output import copy_to_clipboard, write_to_file, write_to_stdout
from src.version import __version__


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pwgen",
        description=t("description"),
        epilog=t("tip_help"),
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=__version__,
        help=t("help_version"),
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=None,
        metavar="N",
        help=t("help_length"),
    )
    parser.add_argument(
        "--count",
        "-n",
        type=int,
        default=None,
        metavar="N",
        help=t("help_count"),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        metavar="FILE",
        help=t("help_output"),
    )
    parser.add_argument(
        "--copy",
        "-c",
        action="store_true",
        help=t("help_copy"),
    )
    parser.add_argument(
        "--passphrase",
        "-p",
        action="store_true",
        help=t("help_passphrase"),
    )
    parser.add_argument(
        "--words",
        "-w",
        type=int,
        default=None,
        metavar="N",
        help=t("help_words"),
    )
    parser.add_argument(
        "--separator",
        type=str,
        default=None,
        metavar="SEP",
        help=t("help_separator"),
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help=t("help_no_digits"),
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help=t("help_no_symbols"),
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help=t("help_no_uppercase"),
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help=t("help_no_lowercase"),
    )
    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help=t("help_no_ambiguous"),
    )

    # Локализация заголовков argparse
    parser._optionals.title = t("options")
    for action in parser._actions:
        if action.dest == "help":
            action.help = t("help_default")
            break

    return parser


def _apply_defaults(args: argparse.Namespace) -> argparse.Namespace:
    file_config = load_config_file()
    cli_values = {
        k: v
        for k, v in {
            "length": args.length,
            "count": args.count,
            "output": args.output,
            "words_count": args.words,
            "separator": args.separator,
            "no_digits": args.no_digits,
            "no_symbols": args.no_symbols,
            "no_uppercase": args.no_uppercase,
            "no_lowercase": args.no_lowercase,
            "no_ambiguous": args.no_ambiguous,
        }.items()
        if v is not None and (not isinstance(v, bool) or v)
    }
    merged = merge_with_cli(file_config or {}, cli_values)

    args.length = merged.get("length", 16)
    args.count = merged.get("count", 1)
    args.output = merged.get("output")
    args.passphrase = args.passphrase or merged.get("passphrase", False)
    args.words_count = merged.get("words_count", 4)
    args.separator = merged.get("separator", "-")
    args.no_digits = merged.get("no_digits", False)
    args.no_symbols = merged.get("no_symbols", False)
    args.no_uppercase = merged.get("no_uppercase", False)
    args.no_lowercase = merged.get("no_lowercase", False)
    args.no_ambiguous = merged.get("no_ambiguous", False)

    return args


def run(args: argparse.Namespace) -> int:
    args = _apply_defaults(args)

    if args.count < 1:
        print(f"Error: {t('error_count')}", file=sys.stderr)
        return 1

    if args.passphrase:
        try:
            passwords = [
                generate_passphrase(
                    words_count=args.words_count,
                    separator=args.separator,
                )
                for _ in range(args.count)
            ]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        try:
            config = GeneratorConfig(
                length=args.length,
                lowercase=not args.no_lowercase,
                uppercase=not args.no_uppercase,
                digits=not args.no_digits,
                symbols=not args.no_symbols,
                no_ambiguous=args.no_ambiguous,
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

        passwords = [
            generate(
                length=config.length,
                lowercase=config.lowercase,
                uppercase=config.uppercase,
                digits=config.digits,
                symbols=config.symbols,
                no_ambiguous=config.no_ambiguous,
            )
            for _ in range(args.count)
        ]

    try:
        if args.output:
            write_to_file(passwords, args.output)
        else:
            write_to_stdout(passwords)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.copy and passwords:
        if copy_to_clipboard(passwords[0]):
            print(t("copy_success"), file=sys.stderr)
        else:
            print(f"Error: {t('error_clipboard')}", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    config = load_config_file()
    if config and "lang" in config:
        set_locale(config.get("lang"))

    parser = _create_parser()
    args = parser.parse_args()
    return run(args)
