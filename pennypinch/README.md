# PennyPinch

A CLI personal finance tracker that logs income and expenses, categorizes
spending, and generates monthly reports — all backed by a single local JSON
file. Zero external dependencies; pure Python standard library.

## Features

- Add income/expense entries with amount, category, date, and optional note
- View all entries, filtered by category and/or date range
- Monthly summary with category-wise spending breakdown and totals
- Persistent storage via a single JSON file (no database setup needed)
- Simple `--help`-driven CLI using only `argparse`

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

Data is stored at `~/.pennypinch.json` by default. Override the path with
`--data path/to/file.json`.