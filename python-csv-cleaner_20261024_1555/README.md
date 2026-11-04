# CSV Cleaner + Email Summary

Drop-in automation script for clients who send messy spreadsheets.

## Usage

```bash
# Basic clean
python csv_cleaner.py messy_data.csv

# With config (date parsing, number parsing, fill rules)
python csv_cleaner.py messy_data.xlsx --config config.json

# Auto-email report + attachment
python csv_cleaner.py data.csv --config config.json --email
```

## Config Options

| Key | Type | Description |
|-----|------|-------------|
| `date_columns` | array | Column names to parse as datetime |
| `numeric_columns` | array | Columns to parse as numbers (strips $, commas) |
| `fill_missing` | object | Per-column: `"drop"`, `"zero"`, `"mean"`, `"forward"` |
| `smtp_*` | string | Gmail/Outlook SMTP credentials (use App Password) |
| `to_emails` | array | Recipient list |

## What It Does

1. Reads CSV or Excel (multiple sheets → first sheet)
2. Strips whitespace, standardizes column names
3. Parses dates/numbers per config
4. Removes duplicates, handles missing values
5. Outputs clean CSV + detailed text report
6. Optionally emails report + clean file as attachment

## Deliver to Client As

- `csv_cleaner.py` + `requirements.txt` + `config.example.json`
- They run: `pip install -r requirements.txt && python csv_cleaner.py their_file.csv --config config.json --email`
- Or you run it for them and send the output