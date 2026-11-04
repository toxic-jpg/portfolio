"""JSON-backed persistence for PennyPinch entries."""

import json
import os

from .models import Entry

DEFAULT_DATA_FILE = os.path.join(os.path.expanduser("~"), ".pennypinch.json")


def load_entries(path: str = DEFAULT_DATA_FILE) -> list[Entry]:
    """Load all entries from the JSON file. Returns [] if missing/empty."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(raw, list):
        return []
    return [Entry.from_dict(item) for item in raw if isinstance(item, dict)]


def save_entries(entries: list[Entry], path: str = DEFAULT_DATA_FILE) -> None:
    """Write all entries to the JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)