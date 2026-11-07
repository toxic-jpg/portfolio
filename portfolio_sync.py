#!/usr/bin/env python3
"""Portfolio sync: auto-scans hermes-portfolio/ for new projects and updates index.html."""

import os
import re
from pathlib import Path

PORTFOLIO_DIR = Path(r"D:\hermes-portfolio")
INDEX_HTML = PORTFOLIO_DIR / "index.html"

# Known project slugs already in the HTML
KNOWN_SLUGS = {
    "python-csv-cleaner",
    "wp-contact-form-7-google-sheets",
    "shopify-section-builder",
    "freelance-automation",
    "java-app-template",
    "vbnet-winforms",
    "forhire-1xcb5t2",
}

def detect_tags(folder):
    tags = set()
    for f in folder.rglob("*"):
        if f.is_file():
            try:
                content = f.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue
            name = f.name.lower()
            if any(x in content or x in name for x in [".py", "python", "pip", "pandas", "numpy", "flask", "django"]):
                tags.add("Python")
            if any(x in content or x in name for x in [".js", "javascript", "node_modules", "webpack", "react", "vue"]):
                tags.add("JavaScript")
            if any(x in content or x in name for x in ["php", "wp-content", "wordpress"]):
                tags.add("PHP")
            if any(x in content or x in name for x in [".java", "swing", "javafx", "maven", "gradle"]):
                tags.add("Java")
            if any(x in content or x in name for x in [".cs", "csharp", "visual-basic", "vbnet", "winforms"]):
                tags.add("VB.NET")
            if any(x in content or x in name for x in ["mysql", "sql", "database", "sqlite", "mariadb"]):
                tags.add("SQL")
            if any(x in content or x in name for x in ["liquid", "shopify"]):
                tags.add("Shopify")
            if any(x in content or x in name for x in ["css", "scss", "tailwind"]):
                tags.add("CSS")
            if any(x in content or x in name for x in ["html", "htm"]):
                tags.add("HTML")
    if not tags:
        tags.add("Web")
    return " · ".join(sorted(tags))


def extract_desc(folder):
    readme = folder / "README.md"
    deploy = folder / "DEPLOY.md"
    if not (readme.exists() or deploy.exists()):
        return "A working project demonstrating software development skills."
    f = readme if readme.exists() else deploy
    lines = f.read_text(encoding="utf-8").splitlines()[:6]
    clean = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped:
            clean.append(stripped)
    desc = " ".join(clean)[:220]
    return desc if desc else ""


def find_new_projects():
    """Find project folders that have not yet been added to the portfolio."""
    # Check index.html for already-added slugs
    if INDEX_HTML.exists():
        html = INDEX_HTML.read_text(encoding="utf-8")
        existing_links = re.findall(r'href="([^"]+)"', html)
        for link in existing_links:
            slug = link.rstrip("/").split("/")[-1]
            if slug:
                KNOWN_SLUGS.add(slug)

    new_cards = []
    for item in PORTFOLIO_DIR.iterdir():
        if not item.is_dir():
            continue
        # Match clean project names, stripping optional _YYYYMMDD_HHMM timestamp suffix
        m = re.match(r"^([a-zA-Z0-9][a-zA-Z0-9_-]*?)(?:_\d{8}_\d{4})?$", item.name)
        if not m:
            continue
        slug = m.group(1)
        if slug in KNOWN_SLUGS:
            continue
        # Skip non-project directories
        has_content = any((item / p).exists() for p in [
            "README.md", "DEPLOY.md", "app.py", "index.html", "app.js",
            ".php", ".java", ".css", ".html", "package.json", "pom.xml",
            ".csproj", ".sln", "requirements.txt"
        ])
        if not has_content:
            continue
        # Try to get title from README
        readme = item / "README.md"
        title = slug.replace("-", " ").title()
        if readme.exists():
            first_line = next((l.strip() for l in readme.read_text().splitlines() if l.startswith("#")), "")
            if first_line:
                title = first_line.lstrip("# ").strip()
        desc = extract_desc(item)
        tags = detect_tags(item)
        new_cards.append({"slug": slug, "title": title, "desc": desc, "tags": tags})
    return new_cards


def update_index_html(new_cards):
    if not new_cards:
        print("[sync] No new projects found.")
        return

    html = INDEX_HTML.read_text(encoding="utf-8")
    for card in new_cards:
        slug = card["slug"]
        title = card["title"]
        desc = card["desc"]
        tags = card["tags"]
        card_block = f'''      <article class="card">
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="tags">{tags}</div>
        <a class="card-link" href="{slug}/" target="_blank" rel="noopener">View →</a>
      </article>
'''
        # Find the last </article> in the card grid and insert after it
        grid_start = html.find('class="card-grid"')
        if grid_start == -1:
            print(f"[sync] ERROR: card-grid not found in index.html")
            return
        # Find the closing div of the card grid
        grid_end = html.find('</div>', grid_start)
        if grid_end == -1:
            print(f"[sync] ERROR: cannot find end of card-grid")
            return
        # Insert before the closing </div>
        html = html[:grid_end] + "\n" + card_block + html[grid_end:]

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"[sync] Added {len(new_cards)} new project(s) to portfolio.")
    for card in new_cards:
        print(f"  - {card['title']} ({card['slug']})")


if __name__ == "__main__":
    new = find_new_projects()
    update_index_html(new)
    print("[sync] Done.")
