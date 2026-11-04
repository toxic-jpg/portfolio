# PennyPinch

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://pypi.org/project/PennyPinch/)

> 💰 **A CLI personal finance tracker. Log income/expenses, categorize spending, and generate monthly reports. Zero dependencies — pure Python standard library.**

No databases. No cloud. No subscriptions. Just you, your money, and a single JSON file.

## Features

- 📝 **Add entries** — Income or expense with amount, category, date, and optional note
- 🔍 **Filter & search** — List entries by category and/or date range
- 📊 **Monthly reports** — Category-wise spending breakdown with totals
- 💾 **Persistent storage** — Single JSON file, no setup required
- ⚡ **Zero dependencies** — Pure Python standard library, nothing to install beyond the package
- 🖥️ **Clean CLI** — `--help`-driven interface using `argparse`

## Install

```bash
pip install -e .
```

This creates a `pennypinch` console command. You can also run it directly:

```bash
python -m pennypinch.cli --help
```

## Usage

```bash
# Add an expense
pennypinch add expense 12.50 --category groceries --note "weekly shop"

# Add income
pennypinch add income 1000 --category salary

# List all entries
pennypinch list

# Filter by category and date range
pennypinch list --category groceries --from 2026-01-01 --to 2026-01-31

# Monthly report
pennypinch report
```

Data is stored at `~/.pennypinch.json` by default. Override the path with `--data path/to/file.json`.

## Project Structure

```
pennypinch/
├── __init__.py
├── cli.py          # Argument parsing and command dispatch
├── models.py       # Data models (Entry, Category, etc.)
└── storage.py      # JSON file read/write
```

## Why PennyPinch?

Most finance apps want your data in the cloud. PennyPinch keeps everything local — your spending history never leaves your machine. The single-file JSON backend means you can back it up, version it with git, or inspect it with any text editor.

## License

MIT