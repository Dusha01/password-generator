import os
from typing import Literal

Locale = Literal["en", "ru"]

_config_locale: Locale | None = None


MESSAGES: dict[Locale, dict[str, str]] = {
    "en": {
        "error_count": "Count must be at least 1",
        "error_clipboard": "Clipboard not available. Install pyperclip: pip install pyperclip",
        "copy_success": "Copied to clipboard",
        "warning_file_readable": "Warning: File is world-readable. Consider: chmod 600 {path}",
        "tip_help": "Tip: Avoid saving passwords in shell history. Use --output to write to a file.",
        "description": "CLI utility for generating cryptographically secure passwords.",
        "help_version": "Show program's version number and exit.",
        "help_length": "Password length (default: 16).",
        "help_count": "Number of passwords to generate (default: 1).",
        "help_output": "Write passwords to file instead of stdout.",
        "help_copy": "Copy first password to clipboard (requires pyperclip).",
        "help_passphrase": "Generate passphrase from words instead of random characters.",
        "help_words": "Number of words for passphrase (default: 4).",
        "help_separator": "Separator between words in passphrase (default: -).",
        "help_no_digits": "Exclude digits.",
        "help_no_symbols": "Exclude special symbols.",
        "help_no_uppercase": "Exclude uppercase letters.",
        "help_no_lowercase": "Exclude lowercase letters.",
        "help_no_ambiguous": "Exclude ambiguous characters (0/O, 1/l/I).",
        "options": "options",
        "help_default": "show this help message and exit",
    },
    "ru": {
        "error_count": "Количество должно быть не менее 1",
        "error_clipboard": "Буфер обмена недоступен. Установите pyperclip: pip install pyperclip",
        "copy_success": "Скопировано в буфер обмена",
        "warning_file_readable": "Внимание: Файл доступен для чтения всем. Рекомендуется: chmod 600 {path}",
        "tip_help": "Совет: Не сохраняйте пароли в истории shell. Используйте --output для записи в файл.",
        "description": "CLI-утилита для генерации криптографически стойких паролей.",
        "help_version": "Показать версию и выйти.",
        "help_length": "Длина пароля (по умолчанию: 16).",
        "help_count": "Количество паролей для генерации (по умолчанию: 1).",
        "help_output": "Записать пароли в файл вместо stdout.",
        "help_copy": "Скопировать первый пароль в буфер обмена (требуется pyperclip).",
        "help_passphrase": "Генерировать парольную фразу из слов вместо случайных символов.",
        "help_words": "Количество слов в парольной фразе (по умолчанию: 4).",
        "help_separator": "Разделитель между словами в парольной фразе (по умолчанию: -).",
        "help_no_digits": "Исключить цифры.",
        "help_no_symbols": "Исключить спецсимволы.",
        "help_no_uppercase": "Исключить заглавные буквы.",
        "help_no_lowercase": "Исключить строчные буквы.",
        "help_no_ambiguous": "Исключить неоднозначные символы (0/O, 1/l/I).",
        "options": "опции",
        "help_default": "показать справку и выйти",
    },
}


def set_locale(locale: str | None) -> None:
    """Устанавливает локаль из конфига (приоритет над LANG)."""
    global _config_locale
    if locale in ("en", "ru"):
        _config_locale = locale  # type: ignore[assignment]
    else:
        _config_locale = None


def get_locale() -> Locale:
    """Определяет локаль: конфиг > LANG env."""
    if _config_locale is not None:
        return _config_locale
    lang = os.environ.get("LANG", "en")
    if lang.startswith("ru"):
        return "ru"
    return "en"


def t(key: str, **kwargs: str) -> str:
    """Возвращает переведённую строку."""
    locale = get_locale()
    msg = MESSAGES[locale].get(key, MESSAGES["en"].get(key, key))
    return msg.format(**kwargs) if kwargs else msg
