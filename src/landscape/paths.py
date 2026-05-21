"""Centralized path constants. One place to swap the storage layout."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent.parent

# Source-controlled config
DATA_DIR: Path = REPO_ROOT / "data"
SOURCES_YAML: Path = DATA_DIR / "sources.yaml"
NANONETS_CONTEXT_MD: Path = DATA_DIR / "nanonets_context.md"
VIEWS_YAML: Path = DATA_DIR / "views.yaml"

# Templates
TEMPLATES_DIR: Path = REPO_ROOT / "templates"

# Rendered output (GitHub Pages root)
DOCS_DIR: Path = REPO_ROOT / "docs"
INDEX_HTML: Path = DOCS_DIR / "index.html"
ABOUT_HTML: Path = DOCS_DIR / "about.html"
ROBOTS_TXT: Path = DOCS_DIR / "robots.txt"
ASSETS_DIR: Path = DOCS_DIR / "assets"
STYLES_CSS: Path = ASSETS_DIR / "styles.css"

# Persistent state (committed)
STATE_DIR: Path = REPO_ROOT / "state"
SEEN_JSON: Path = STATE_DIR / "seen.json"
QUESTIONS_MD: Path = STATE_DIR / "questions_for_team.md"

# Per-build ephemera (gitignored)
RUN_DIR: Path = STATE_DIR / "run"
LOCK_FILE: Path = STATE_DIR / ".lock"

ITEMS_RAW: Path = RUN_DIR / "items_raw.jsonl"
ITEMS_DEDUPED: Path = RUN_DIR / "items_deduped.jsonl"
ITEMS_SCORED: Path = RUN_DIR / "items_scored.jsonl"
ITEMS_FRAMED: Path = RUN_DIR / "items_framed.jsonl"
EDITION_JSON: Path = RUN_DIR / "edition.json"


def per_audience_html(audience: str) -> Path:
    """Return the docs/ path for a per-audience HTML view."""
    return DOCS_DIR / f"for-{audience}.html"


def ensure_dirs() -> None:
    """Create any missing directories. Safe to call repeatedly."""
    for d in (DATA_DIR, TEMPLATES_DIR, DOCS_DIR, ASSETS_DIR, STATE_DIR, RUN_DIR):
        d.mkdir(parents=True, exist_ok=True)
