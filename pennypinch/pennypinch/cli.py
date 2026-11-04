"""Argparse-driven CLI for PennyPinch."""

import argparse
import sys
from collections import defaultdict
from datetime import date, datetime

from . import storage
from .models import Entry


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _filter(entries, category=None, start=None, end=None):
    result = []
    for e in entries:
        d = datetime.strptime(e.date, "%Y-%m-%d").date()
        if category and e.category != category:
            continue
        if start and d < start:
            continue
        if end and d > end:
            continue
        result.append(e)
    return result


def _cmd_add(args):
    entry = Entry(
        type=args.type,
        amount=args.amount,
        category=args.category,
        date=args.date or date.today().isoformat(),
        note=args.note or "",
    )
    entries = storage.load_entries(args.data)
    entries.append(entry)
    storage.save_entries(entries, args.data)
    print(f"Added {entry.type} of {entry.amount:.2f} in '{entry.category}' on {entry.date}.")


def _cmd_list(args):
    entries = storage.load_entries(args.data)
    entries = _filter(
        entries,
        category=args.category,
        start=args.start,
        end=args.end,
    )
    if not entries:
        print("No entries found.")
        return
    print(f"{'Date':<12} {'Type':<9} {'Amount':>10}  {'Category':<15} Note")
    print("-" * 70)
    for e in sorted(entries, key=lambda x: x.date):
        print(f"{e.date:<12} {e.type:<9} {e.amount:>10.2f}  {e.category:<15} {e.note}")


def _cmd_report(args):
    entries = storage.load_entries(args.data)
    entries = _filter(
        entries,
        category=args.category,
        start=args.start,
        end=args.end,
    )
    if not entries:
        print("No entries found for this period.")
        return

    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "cats": defaultdict(float)})
    for e in entries:
        month = e.date[:7]  # YYYY-MM
        monthly[month][e.type] += e.amount
        monthly[month]["cats"][e.category] += e.amount

    for month in sorted(monthly):
        data = monthly[month]
        net = data["income"] - data["expense"]
        print(f"\n=== {month} ===")
        print(f"Income:  {data['income']:>10.2f}")
        print(f"Expense: {data['expense']:>10.2f}")
        print(f"Net:     {net:>10.2f}")
        print("Category breakdown:")
        for cat in sorted(data["cats"]):
            print(f"  {cat:<15} {data['cats'][cat]:>10.2f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pennypinch",
        description="PennyPinch — CLI personal finance tracker.",
    )
    parser.add_argument(
        "--data",
        default=storage.DEFAULT_DATA_FILE,
        help="Path to the JSON data file (default: ~/.pennypinch.json).",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # add
    add = sub.add_parser("add", help="Add an income or expense entry.")
    add.add_argument("type", choices=["income", "expense"], help="Entry type.")
    add.add_argument("amount", type=float, help="Amount (e.g. 12.50).")
    add.add_argument("category", help="Category (e.g. groceries, salary).")
    add.add_argument("--date", help="Date YYYY-MM-DD (default: today).")
    add.add_argument("--note", help="Optional note.")
    add.set_defaults(func=_cmd_add)

    # list
    lst = sub.add_parser("list", help="List entries, optionally filtered.")
    lst.add_argument("--category", help="Filter by category.")
    lst.add_argument("--from", dest="start", type=_parse_date, help="Start date YYYY-MM-DD.")
    lst.add_argument("--to", dest="end", type=_parse_date, help="End date YYYY-MM-DD.")
    lst.set_defaults(func=_cmd_list)

    # report
    rep = sub.add_parser("report", help="Monthly summary report.")
    rep.add_argument("--category", help="Filter by category.")
    rep.add_argument("--from", dest="start", type=_parse_date, help="Start date YYYY-MM-DD.")
    rep.add_argument("--to", dest="end", type=_parse_date, help="End date YYYY-MM-DD.")
    rep.set_defaults(func=_cmd_report)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()