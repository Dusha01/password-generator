# password-generator

A command-line utility for generating cryptographically secure passwords and passphrases.

**[Русская версия](README.ru.md)**

## Features

- **Cryptographically secure** — Uses Python's `secrets` module (CSPRNG)
- **Password mode** — Random characters with configurable character sets
- **Passphrase mode** — Memorable passphrases from EFF wordlist (1296 words)
- **Flexible output** — stdout, file, or clipboard
- **Configuration file** — Persistent defaults via JSON config
- **Internationalization** — English and Russian (locale from `LANG`)

## Requirements

- Python 3.10+
- Optional: `pyperclip` for clipboard support (`--copy`)

## Installation

Run all commands from the project root directory (`password-generator/`).

### Method 1: pip (recommended for global use)

Install so `pwgen` is available in any terminal:

```bash
cd password-generator
pip install -e .
```

With clipboard support:

```bash
pip install -e ".[clipboard]"
```

If the above fails, install pyperclip separately:

```bash
pip install -e .
pip install -r requirements-clipboard.txt
```

### Method 2: pipx (isolated, recommended for CLI tools)

```bash
pipx install -e .
# With clipboard:
pipx inject password-generator pyperclip
```

### Method 3: Virtual environment

```bash
cd password-generator
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -e ".[clipboard]"
```

Then either:
- Activate the venv before each use: `source .venv/bin/activate` → `pwgen`
- Or add the venv to PATH (e.g. in `~/.bashrc`): `export PATH="$HOME/Projects/CLI/password-generator/.venv/bin:$PATH"`

### Verify installation

```bash
pwgen --version
# or
pwgen --help
```

If `pwgen` is not found, ensure the Python scripts directory is in your PATH:
- `~/.local/bin` (pip install --user)
- `~/.venv/bin` (when using venv)

Add to `~/.bashrc` or `~/.zshrc` if needed:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Development dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
# Generate a 16-character password (default)
pwgen

# Generate a 24-character password without symbols
pwgen --length 24 --no-symbols

# Generate a 4-word passphrase
pwgen --passphrase

# Generate 5 passwords and save to file
pwgen --count 5 --output passwords.txt

# Copy password to clipboard
pwgen --copy
```

## Usage

### Password Mode

Generate random passwords with configurable character sets:

```bash
pwgen                          # Default: 16 chars, all character types
pwgen -l 32                    # 32 characters
pwgen -l 20 --no-symbols       # Alphanumeric only
pwgen -l 16 --no-ambiguous     # Exclude 0/O, 1/l/I
pwgen -l 12 --no-digits        # Letters and symbols only
```

### Passphrase Mode

Generate memorable passphrases from the EFF short wordlist:

```bash
pwgen -p                       # 4 words, hyphen separator
pwgen -p -w 6                  # 6 words
pwgen -p -w 5 --separator "_"  # 5 words, underscore separator
```

### Output Options

```bash
pwgen -n 3                     # Generate 3 passwords
pwgen -o secrets.txt           # Write to file
pwgen -c                       # Copy first to clipboard (requires pyperclip)
```

## Configuration File

Set persistent defaults by creating a config file. The tool looks for (first found wins):

1. **Project** `./.config/pwgen/config.json` (directory of the installed package — used when running via `pipx` from anywhere)
2. **Project** `./.pwgenrc`
3. **Current dir** `./.config/pwgen/config.json`
4. **Current dir** `./.pwgenrc`
5. **Home** `~/.config/pwgen/config.json`
6. **Home** `~/.pwgenrc`

Example `~/.config/pwgen/config.json`:

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

- **lang** — Interface language: `"en"` or `"ru"` (overrides `LANG` env)
- CLI arguments override config file values

## Command-Line Reference

| Option | Short | Description | Default |
|--------|-------|--------------|---------|
| `--length` | `-l` | Password length | 16 |
| `--count` | `-n` | Number of passwords to generate | 1 |
| `--output` | `-o` | Write to file instead of stdout | — |
| `--copy` | `-c` | Copy first password to clipboard | — |
| `--passphrase` | `-p` | Generate passphrase from words | false |
| `--words` | `-w` | Number of words in passphrase | 4 |
| `--separator` | — | Word separator in passphrase | `-` |
| `--no-digits` | — | Exclude digits | false |
| `--no-symbols` | — | Exclude special symbols | false |
| `--no-uppercase` | — | Exclude uppercase letters | false |
| `--no-lowercase` | — | Exclude lowercase letters | false |
| `--no-ambiguous` | — | Exclude ambiguous chars (0/O, 1/l/I) | false |
| `--version` | `-v` | Show version | — |
| `--help` | `-h` | Show help | — |

## Internationalization

The tool supports English and Russian. The locale is detected from the `LANG` environment variable:

```bash
LANG=ru_RU.UTF-8 pwgen --help   # Russian messages
LANG=en_US.UTF-8 pwgen --help   # English messages
```

## Security

- **CSPRNG only** — Uses `secrets` module, never `random`
- **No logging** — Passwords are never logged
- **File permissions** — Warns when output file is world-readable
- **Shell history** — Tip in help: avoid saving passwords in history; use `--output` for files

## Development

### Project Structure

```
password-generator/
├── src/
│   ├── core/           # CLI, config, validation
│   ├── modules/
│   │   ├── generator/  # Password & passphrase generation
│   │   └── output/     # stdout, file, clipboard
│   ├── i18n.py
│   └── version.py
├── tests/
├── docs/
├── run.py              # Dev entry point
└── pyproject.toml
```

### Run from source

```bash
python run.py --help
python run.py --passphrase
```

### Run tests

```bash
pytest tests/ -v
```

### Release

Releases are automated via GitHub Actions. To create a release:

1. Update version in `pyproject.toml` (единственный источник истины)
2. Commit and push changes
3. Create and push a tag:

```bash
git tag v0.1.1
git push origin v0.1.1
```

The workflow will run tests, build the package, and create a GitHub Release with wheel and sdist artifacts.

## License

MIT License — see [LICENSE](LICENSE) for details.
