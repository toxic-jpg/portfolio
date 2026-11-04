#!/usr/bin/env python3
"""
CSV Cleaner + Email Summary
Reads messy CSV/Excel → cleans → outputs clean CSV + emails summary report.
"""
import pandas as pd
import smtplib
import argparse
import sys
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

def clean_dataframe(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, dict]:
    """Apply cleaning steps. Returns (cleaned_df, report_dict)."""
    report = {
        "original_rows": len(df),
        "original_cols": list(df.columns),
        "steps": []
    }
    
    # 1. Strip whitespace from column names
    df.columns = df.columns.str.strip()
    report["steps"].append("Stripped column name whitespace")
    
    # 2. Drop completely empty rows/cols
    df = df.dropna(how='all').dropna(axis=1, how='all')
    report["steps"].append(f"Dropped empty rows/cols: {report['original_rows']} → {len(df)} rows")
    
    # 3. Standardize column names (lowercase, underscores)
    df.columns = df.columns.str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True).str.strip('_')
    report["steps"].append("Standardized column names")
    
    # 4. Parse dates (configurable)
    date_cols = config.get("date_columns", [])
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            report["steps"].append(f"Parsed dates in '{col}'")
    
    # 5. Parse numbers (remove $, commas, etc.)
    num_cols = config.get("numeric_columns", [])
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r'[$,£€]', '', regex=True).str.replace(',', ''),
                errors='coerce'
            )
            report["steps"].append(f"Parsed numbers in '{col}'")
    
    # 6. Remove duplicates
    dup_count = df.duplicated().sum()
    if dup_count:
        df = df.drop_duplicates()
        report["steps"].append(f"Removed {dup_count} duplicate rows")
    
    # 7. Fill/handle missing values
    fill_config = config.get("fill_missing", {})
    for col, strategy in fill_config.items():
        if col in df.columns:
            if strategy == "drop":
                before = len(df)
                df = df.dropna(subset=[col])
                report["steps"].append(f"Dropped {before - len(df)} rows missing '{col}'")
            elif strategy == "zero":
                df[col] = df[col].fillna(0)
                report["steps"].append(f"Filled missing '{col}' with 0")
            elif strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
                report["steps"].append(f"Filled missing '{col}' with mean")
            elif strategy == "forward":
                df[col] = df[col].ffill()
                report["steps"].append(f"Forward-filled missing '{col}'")
    
    # 8. Text cleanup
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().replace('nan', '')
    report["steps"].append("Trimmed whitespace from text columns")
    
    report["final_rows"] = len(df)
    report["final_cols"] = list(df.columns)
    report["missing_counts"] = df.isnull().sum().to_dict()
    
    return df, report

def generate_report(report: dict, input_file: str, output_file: str) -> str:
    lines = [
        f"CSV Cleaner Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Input: {input_file}",
        f"Output: {output_file}",
        "",
        f"Original: {report['original_rows']} rows × {len(report['original_cols'])} cols",
        f"Final:   {report['final_rows']} rows × {len(report['final_cols'])} cols",
        "",
        "Steps applied:",
    ]
    for i, step in enumerate(report["steps"], 1):
        lines.append(f"  {i}. {step}")
    
    lines.extend(["", "Missing values per column:"])
    for col, count in report["missing_counts"].items():
        if count:
            lines.append(f"  {col}: {count}")
    
    return "
".join(lines)

def send_email(config: dict, report_text: str, attachment_path: str = None):
    msg = MIMEMultipart()
    msg['Subject'] = f"CSV Cleaner Report — {Path(config['input']).name}"
    msg['From'] = config['smtp_user']
    msg['To'] = ", ".join(config['to_emails'])
    
    msg.attach(MIMEText(report_text, 'plain'))
    
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=Path(attachment_path).name)
        part['Content-Disposition'] = f'attachment; filename="{Path(attachment_path).name}"'
        msg.attach(part)
    
    with smtplib.SMTP(config['smtp_host'], config['smtp_port']) as server:
        server.starttls()
        server.login(config['smtp_user'], config['smtp_pass'])
        server.send_message(msg)

def main():
    parser = argparse.ArgumentParser(description="Clean CSV/Excel and email summary")
    parser.add_argument("input", help="Input CSV or Excel file")
    parser.add_argument("-o", "--output", help="Output CSV file (default: input_cleaned.csv)")
    parser.add_argument("--config", help="JSON config file for cleaning rules")
    parser.add_argument("--email", action="store_true", help="Send email report")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)
    
    output_path = Path(args.output) if args.output else input_path.with_stem(input_path.stem + "_cleaned").with_suffix(".csv")
    
    # Load config
    config = {
        "date_columns": [],
        "numeric_columns": [],
        "fill_missing": {},
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
    }
    if args.config:
        with open(args.config) as f:
            config.update(json.load(f))
    
    # Read input
    if input_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)
    
    # Clean
    df_clean, report = clean_dataframe(df, config)
    
    # Save
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    
    # Report
    report_text = generate_report(report, str(input_path), str(output_path))
    print("
" + report_text)
    
    # Email
    if args.email:
        if not all(k in config for k in ['smtp_user', 'smtp_pass', 'to_emails']):
            print("Error: Email config incomplete (need smtp_user, smtp_pass, to_emails)")
        else:
            send_email(config, report_text, str(output_path))
            print("Email sent!")

if __name__ == "__main__":
    import json
    main()