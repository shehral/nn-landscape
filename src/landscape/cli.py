"""CLI entry points. Each command is the contract the build agent calls."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from pathlib import Path

import typer

from .dedup import (
    apply_source_boost,
    group_by_canonical_url,
    merge_jaccard_near_duplicates,
)
from .ingest import load_sources, run_sources
from .models import (
    AIQuestion,
    AxisScores,
    EditionJSON,
    Framing,
    Item,
    TrendBullet,
)
from .paths import (
    EDITION_JSON,
    ITEMS_DEDUPED,
    ITEMS_RAW,
    ITEMS_SCORED,
    RUN_DIR,
    SOURCES_YAML,
    ensure_dirs,
)
from .render import render_all

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Nanonets Landscape Monitor — CLI for the build pipeline.")


def _write_jsonl(items: Iterable[Item], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(item.model_dump_json() + "\n")
            n += 1
    return n


def _read_jsonl(path: Path) -> Iterator[Item]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                yield Item.model_validate_json(stripped)


@app.command()
def ingest() -> None:
    """Fetch items from every source in data/sources.yaml. Write items_raw.jsonl."""
    ensure_dirs()
    sources = load_sources(SOURCES_YAML)
    items, failures, covered = run_sources(sources)
    n = _write_jsonl(items, ITEMS_RAW)
    typer.echo(f"ingest: {n} items written to {ITEMS_RAW}")
    typer.echo(f"  covered: {', '.join(covered) or '(none)'}")
    if failures:
        for f in failures:
            typer.echo(f"  FAILED {f.source}: {f.error}")


@app.command()
def dedup() -> None:
    """Run the 3-function dedup pipeline. Write items_deduped.jsonl."""
    items = list(_read_jsonl(ITEMS_RAW))
    s1 = group_by_canonical_url(items)
    s2 = merge_jaccard_near_duplicates(s1)
    s3 = apply_source_boost(s2)
    n = _write_jsonl(s3, ITEMS_DEDUPED)
    typer.echo(f"dedup: {len(items)} -> {n} items (grouped {len(items) - len(s1)}, jaccard-merged {len(s1) - len(s2)})")


def _stub_score(item: Item) -> Item:
    """Deterministic synthetic scoring for Phase A end-to-end runs."""
    h = int(hashlib.sha256(item.id.encode()).hexdigest()[:16], 16)
    scores = AxisScores(
        doc_ai=h % 6,
        competitive=(h >> 4) % 6,
        frontier=(h >> 8) % 6,
        vlm_research=(h >> 12) % 6,
    )
    axis_dict = scores.model_dump()
    primary = max(axis_dict, key=lambda k: axis_dict[k])
    composite = (
        scores.doc_ai * 0.35
        + scores.competitive * 0.30
        + scores.frontier * 0.20
        + scores.vlm_research * 0.15
    ) * 20.0
    return item.model_copy(
        update={
            "axis_scores": scores,
            "primary_axis": primary,
            "composite_score": composite,
            "one_line_summary": f"[stub] {item.title[:120]}",
            "framing": Framing(
                product_implication="[stub product implication — Phase B replaces this.]",
                research_implication="[stub research implication — Phase B replaces this.]",
                action_recommendation="[stub action — Phase B replaces this.]",
            )
            if composite >= 60.0
            else None,
        }
    )


@app.command()
def score_stub() -> None:
    """Phase A only: synthetic deterministic scoring so render can be exercised."""
    items = [_stub_score(item) for item in _read_jsonl(ITEMS_DEDUPED)]
    n = _write_jsonl(items, ITEMS_SCORED)
    typer.echo(f"score-stub: {n} items scored")


@app.command()
def render() -> None:
    """Read edition.json and write the three audience views + about.html."""
    edition = EditionJSON.model_validate_json(EDITION_JSON.read_text())
    outputs = render_all(edition)
    for name, path in outputs.items():
        typer.echo(f"render: {name} -> {path.relative_to(path.parent.parent)}")


@app.command()
def build(
    stub: bool = typer.Option(False, "--stub", help="Use synthetic scoring; skip LLM calls."),
) -> None:
    """Orchestrate ingest -> dedup -> [score-stub | score-real] -> render.

    Phase A: --stub. Phase B: real LLM scoring + framing + trend + AI-partner.
    """
    ensure_dirs()
    ingest()
    dedup()
    if not stub:
        typer.echo("build: real-LLM scoring not implemented yet (Phase B). Use --stub.")
        raise typer.Exit(1)
    score_stub()

    items = list(_read_jsonl(ITEMS_SCORED))
    edition = EditionJSON(
        built_at=datetime.now(UTC),
        sources_covered=("arxiv", "hn", "rss", "github_trending"),
        items=tuple(items),
        trend_bullets=(
            TrendBullet(summary="[stub trend bullet 1 — Phase B replaces this.]", evidence_item_ids=()),
            TrendBullet(summary="[stub trend bullet 2 — Phase B replaces this.]", evidence_item_ids=()),
            TrendBullet(summary="[stub trend bullet 3 — Phase B replaces this.]", evidence_item_ids=()),
        ),
        ai_partner_questions=(
            AIQuestion(
                question="[stub AI-partner question — Phase B replaces this.]",
                context="[stub context — Phase B replaces this.]",
            ),
        ),
        audit_passed=True,
    )
    EDITION_JSON.write_text(edition.model_dump_json(indent=2), encoding="utf-8")
    typer.echo(f"build: edition.json -> {EDITION_JSON}")
    render()


if __name__ == "__main__":
    app()
