"""Business website with contact form — deliverable for r/forhire job 1xcb5t2.

Run:  pip install -r requirements.txt && python app.py
Then: http://127.0.0.1:5000
"""
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "submissions.db"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
MAX_LEN = {"name": 80, "email": 160, "message": 4000}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024  # 32 KB cap on any request body


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                ip TEXT,
                user_agent TEXT
            )
            """
        )


init_db()


@app.get("/")
def index():
    return render_template("index.html", site=SITE.copy())


@app.post("/api/contact")
def contact():
    payload = request.get_json(silent=True) or {}
    errors = {}

    for field in ("name", "email", "message"):
        value = str(payload.get(field, "")).strip()
        if not value:
            errors[field] = "This field is required."
        elif len(value) > MAX_LEN[field]:
            errors[field] = f"Keep it under {MAX_LEN[field]} characters."
        else:
            payload[field] = value

    if "email" not in errors and not EMAIL_RE.match(payload["email"]):
        errors["email"] = "That email address doesn't look right."

    if errors:
        return jsonify({"ok": False, "errors": errors}), 422

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO contacts (name, email, message, created_at, ip, user_agent) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                payload["name"],
                payload["email"],
                payload["message"],
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                request.headers.get("X-Forwarded-For", request.remote_addr),
                request.headers.get("User-Agent", "")[:300],
            ),
        )

    # Mirror to a JSONL file so the owner can read leads without SQL tooling.
    lead = {
        "name": payload["name"],
        "email": payload["email"],
        "message": payload["message"],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with (DB_PATH.parent / "leads.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(lead, ensure_ascii=False) + "\n")

    return jsonify({"ok": True, "message": "Thanks — I'll get back to you within a day."})


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True})


# --- Editable site content -------------------------------------------------
SITE = {
    "business_name": "Your Business Name",
    "tagline": " Honest, dependable service for homes and small businesses.",
    "about": (
        "We take on the jobs other shops turn down. Straight quotes, no hidden "
        "fees, and a call back when we say we will."
    ),
    "services": [
        {"title": "Repairs & Maintenance", "detail": "Diagnosis, parts, and labour quoted up front."},
        {"title": "Installations", "detail": "Supply and fit, with a 12-month workmanship guarantee."},
        {"title": "Consultations", "detail": "A honest second opinion before you spend."},
    ],
    "phone": "+63 000 000 0000",
    "email": "hello@example.com",
    "hours": "Mon–Sat, 8:00–18:00",
    "address": "Your City, Philippines",
}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)