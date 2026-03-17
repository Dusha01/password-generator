# password-generator

Консольная утилита для генерации криптографически стойких паролей и парольных фраз.

**[English version](README.md)**

## Возможности

- **Криптографическая стойкость** — использует модуль `secrets` (CSPRNG)
- **Режим пароля** — случайные символы с настраиваемым набором
- **Режим парольной фразы** — запоминаемые фразы из списка EFF (1296 слов)
- **Гибкий вывод** — stdout, файл или буфер обмена
- **Файл конфигурации** — постоянные настройки по умолчанию
- **Локализация** — русский и английский (по переменной `LANG`)

## Требования

- Python 3.10+
- Опционально: `pyperclip` для копирования в буфер (`--copy`)

## Установка

Все команды выполняйте из корня проекта (`password-generator/`).

### Способ 1: pip (рекомендуется для глобального использования)

Установка, чтобы команда `pwgen` была доступна в любом терминале:

```bash
cd password-generator
pip install -e .
```

С поддержкой буфера обмена:

```bash
pip install -e ".[clipboard]"
```

Если команда выше не сработала, установите pyperclip отдельно:

```bash
pip install -e .
pip install -r requirements-clipboard.txt
```

### Способ 2: pipx (изолированная установка, удобно для CLI)

```bash
pipx install -e .
# С буфером обмена:
pipx inject password-generator pyperclip
```

### Способ 3: Виртуальное окружение

```bash
cd password-generator
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -e ".[clipboard]"
```

Далее либо:
- Активируйте venv перед каждым запуском: `source .venv/bin/activate` → `pwgen`
- Либо добавьте venv в PATH (например, в `~/.bashrc`): `export PATH="$HOME/Projects/CLI/password-generator/.venv/bin:$PATH"`

### Проверка установки

```bash
pwgen --version
# или
pwgen --help
```

Если `pwgen` не находится, проверьте, что каталог со скриптами Python в PATH:
- `~/.local/bin` (при pip install --user)
- `~/.venv/bin` (при использовании venv)

При необходимости добавьте в `~/.bashrc` или `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Зависимости для разработки

```bash
pip install -e ".[dev]"
```

## Быстрый старт

```bash
# Сгенерировать пароль из 16 символов (по умолчанию)
pwgen

# Пароль из 24 символов без спецсимволов
pwgen --length 24 --no-symbols

# Парольная фраза из 4 слов
pwgen --passphrase

# 5 паролей в файл
pwgen --count 5 --output passwords.txt

# Копировать в буфер обмена
pwgen --copy
```

## Использование

### Режим пароля

Генерация случайных паролей с настраиваемым набором символов:

```bash
pwgen                          # По умолчанию: 16 символов, все типы
pwgen -l 32                    # 32 символа
pwgen -l 20 --no-symbols       # Только буквы и цифры
pwgen -l 16 --no-ambiguous     # Без 0/O, 1/l/I
pwgen -l 12 --no-digits        # Только буквы и спецсимволы
```

### Режим парольной фразы

Генерация запоминаемых фраз из списка EFF:

```bash
pwgen -p                       # 4 слова, разделитель «-»
pwgen -p -w 6                  # 6 слов
pwgen -p -w 5 --separator "_"  # 5 слов, разделитель «_»
```

### Вывод

```bash
pwgen -n 3                     # Сгенерировать 3 пароля
pwgen -o secrets.txt           # Записать в файл
pwgen -c                       # Копировать первый в буфер (нужен pyperclip)
```

## Файл конфигурации

Настройки по умолчанию можно задать в конфиге. Утилита ищет файлы (используется первый найденный):

1. **Проект** `./.config/pwgen/config.json` (директория установленного пакета — используется при запуске через `pipx` из любой папки)
2. **Проект** `./.pwgenrc`
3. **Текущая папка** `./.config/pwgen/config.json`
4. **Текущая папка** `./.pwgenrc`
5. **Домашняя** `~/.config/pwgen/config.json`
6. **Домашняя** `~/.pwgenrc`

Пример `~/.config/pwgen/config.json`:

```json
{
  "lang": "ru",
  "length": 20,
  "no_symbols": false,
  "no_ambiguous": false,
  "passphrase": false,
  "words_count": 4,
  "separator": "-",
  "no_digits": false,
  "no_uppercase": false,
  "no_lowercase": false
}
```

- **lang** — Язык интерфейса: `"en"` или `"ru"` (имеет приоритет над переменной `LANG`)
- Аргументы командной строки переопределяют значения из конфига

## Справка по опциям

| Опция | Короткая | Описание | По умолчанию |
|-------|----------|----------|--------------|
| `--length` | `-l` | Длина пароля | 16 |
| `--count` | `-n` | Количество паролей | 1 |
| `--output` | `-o` | Записать в файл | — |
| `--copy` | `-c` | Копировать первый в буфер | — |
| `--passphrase` | `-p` | Генерировать парольную фразу | false |
| `--words` | `-w` | Количество слов во фразе | 4 |
| `--separator` | — | Разделитель слов | `-` |
| `--no-digits` | — | Исключить цифры | false |
| `--no-symbols` | — | Исключить спецсимволы | false |
| `--no-uppercase` | — | Исключить заглавные буквы | false |
| `--no-lowercase` | — | Исключить строчные буквы | false |
| `--no-ambiguous` | — | Исключить 0/O, 1/l/I | false |
| `--version` | `-v` | Показать версию | — |
| `--help` | `-h` | Справка | — |

## Локализация

Поддерживаются русский и английский. Язык определяется по переменной `LANG`:

```bash
LANG=ru_RU.UTF-8 pwgen --help   # Сообщения на русском
LANG=en_US.UTF-8 pwgen --help   # Сообщения на английском
```

## Безопасность

- **Только CSPRNG** — используется модуль `secrets`, не `random`
- **Без логирования** — пароли не записываются в логи
- **Права доступа** — предупреждение при записи в файл, доступный всем
- **История shell** — в справке совет: не сохранять пароли в истории; для файлов использовать `--output`

## Разработка

### Структура проекта

```
password-generator/
├── src/
│   ├── core/           # CLI, конфиг, валидация
│   ├── modules/
│   │   ├── generator/  # Генерация паролей и фраз
│   │   └── output/     # stdout, файл, буфер обмена
│   ├── i18n.py
│   └── version.py
├── tests/
├── docs/
├── run.py              # Точка входа для разработки
└── pyproject.toml
```

### Запуск из исходников

```bash
python run.py --help
python run.py --passphrase
```

### Запуск тестов

```bash
pytest tests/ -v
```

### Релиз

Релизы автоматизированы через GitHub Actions. Чтобы создать релиз:

1. Обнови версию в `pyproject.toml` (единственный источник истины)
2. Закоммить и запушь изменения
3. Создай и запушь тег:

```bash
git tag v1.0.1
git push origin v1.0.1
```

Workflow запустит тесты, соберёт пакет и создаст GitHub Release с артефактами.

## Лицензия

MIT License — см. [LICENSE](LICENSE).
