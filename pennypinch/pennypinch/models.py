"""Data model for financial entries."""

from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Entry:
    """A single income or expense entry."""

    type: str       # "income" or "expense"
    amount: float
    category: str
    date: str       # ISO YYYY-MM-DD
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        return cls(
            type=data["type"],
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"],
            note=data.get("note", ""),
        )