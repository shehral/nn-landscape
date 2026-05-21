"""Jinja2 renderer. Audience views re-weight at render time (no re-scoring)."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import Axis, EditionJSON, Item
from .paths import (
    ABOUT_HTML,
    DOCS_DIR,
    INDEX_HTML,
    TEMPLATES_DIR,
    VIEWS_YAML,
    per_audience_html,
)

AXIS_COLUMNS: list[tuple[Axis, str]] = [
    ("doc_ai", "Document AI"),
    ("competitive", "Competitive"),
    ("frontier", "Frontier"),
    ("vlm_research", "VLM research"),
]

REPO_URL = "https://github.com/shehral/nn-landscape"
QUESTIONS_FILE_URL = f"{REPO_URL}/blob/main/state/questions_for_team.md"
QUESTIONS_EDIT_URL = f"{REPO_URL}/edit/main/state/questions_for_team.md"
CONTEXT_FILE_URL = f"{REPO_URL}/blob/main/data/nanonets_context.md"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _view_score(item: Item, weights: dict[str, float]) -> float:
    """Re-weight an item's 0..5 axis scores into a 0..100 composite for this view."""
    if item.axis_scores is None:
        return 0.0
    total_w = sum(weights.values()) or 1.0
    weighted_sum = sum(getattr(item.axis_scores, axis) * w for axis, w in weights.items())
    return (weighted_sum / total_w) * 20.0


def _select_with_quota(
    scored: list[tuple[float, Item]], top_n: int, min_per_axis: int
) -> list[Item]:
    """Quota-fill so high-weighted axes never starve. Sort the final list by score."""
    by_axis: dict[Axis, list[tuple[float, Item]]] = defaultdict(list)
    for score, item in scored:
        if item.primary_axis is not None:
            by_axis[item.primary_axis].append((score, item))

    selected: list[tuple[float, Item]] = []
    seen: set[str] = set()

    for items in by_axis.values():
        for score, item in items[:min_per_axis]:
            if item.id not in seen:
                selected.append((score, item))
                seen.add(item.id)

    remaining = top_n - len(selected)
    for score, item in scored:
        if remaining <= 0:
            break
        if item.id not in seen:
            selected.append((score, item))
            seen.add(item.id)
            remaining -= 1

    selected.sort(key=lambda x: x[0], reverse=True)
    return [item.model_copy(update={"composite_score": score}) for score, item in selected]


def _group_by_axis(items: list[Item]) -> dict[Axis, list[Item]]:
    groups: dict[Axis, list[Item]] = {axis: [] for axis, _ in AXIS_COLUMNS}
    for item in items:
        if item.primary_axis is not None:
            groups[item.primary_axis].append(item)
    return groups


def load_views() -> dict[str, dict]:
    return yaml.safe_load(VIEWS_YAML.read_text())["views"]


def render_view(
    edition: EditionJSON, view_name: str, view_config: dict, out_path: Path
) -> str:
    """Render one audience view to out_path. Returns the rendered HTML string."""
    weights = view_config["axis_weights"]
    scored = [(_view_score(item, weights), item) for item in edition.items]
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = _select_with_quota(
        scored, view_config["top_n_overall"], view_config["min_per_axis"]
    )

    env = _env()
    template = env.get_template("edition.html.j2")
    html = template.render(
        view=view_config,
        items_by_axis=_group_by_axis(selected),
        axis_columns=AXIS_COLUMNS,
        trend_bullets=edition.trend_bullets,
        ai_partner_questions=edition.ai_partner_questions,
        sources_covered=list(edition.sources_covered),
        sources_failed=list(edition.sources_failed),
        audit_passed=edition.audit_passed,
        built_at_iso=edition.built_at.isoformat(),
        built_at_human=edition.built_at.strftime("%b %d, %Y · %H:%M UTC"),
        questions_file_url=QUESTIONS_FILE_URL,
        questions_edit_url=QUESTIONS_EDIT_URL,
        context_file_url=CONTEXT_FILE_URL,
    )
    out_path.write_text(html, encoding="utf-8")
    return html


def render_about() -> str:
    """Render the About page (static content; no per-build data)."""
    env = _env()
    template = env.get_template("about.html.j2")
    html = template.render()
    ABOUT_HTML.write_text(html, encoding="utf-8")
    return html


def render_all(edition: EditionJSON) -> dict[str, Path]:
    """Render every configured view. Returns name -> written-path."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    views = load_views()
    outputs: dict[str, Path] = {}
    for name, conf in views.items():
        out_path = INDEX_HTML if name == "default" else per_audience_html(name)
        render_view(edition, name, conf, out_path)
        outputs[name] = out_path
    render_about()
    outputs["about"] = ABOUT_HTML
    return outputs
