"""CLI entry points. Each command is the contract the build agent calls."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
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
    LOCK_FILE,
    QUESTIONS_MD,
    REPO_ROOT,
    RUN_DIR,
    SEEN_JSON,
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


@app.command()
def lock(
    acquire: bool = typer.Option(False, "--acquire"),
    release: bool = typer.Option(False, "--release"),
) -> None:
    """Acquire or release the build lock (state/.lock).

    Acquire writes the current PID. If the lock exists with a live PID, abort.
    If the lock exists with a dead PID (e.g., previous build crashed), clear it.
    Release removes the lock file.
    """
    if acquire == release:
        typer.echo("specify exactly one of --acquire / --release", err=True)
        raise typer.Exit(2)

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if release:
        LOCK_FILE.unlink(missing_ok=True)
        typer.echo("lock: released")
        return

    if LOCK_FILE.exists():
        try:
            existing_pid = int(LOCK_FILE.read_text().strip())
        except (ValueError, OSError):
            existing_pid = -1
        if existing_pid > 0:
            try:
                os.kill(existing_pid, 0)
                typer.echo(f"lock: another build is in progress (PID {existing_pid})", err=True)
                raise typer.Exit(1)
            except ProcessLookupError:
                pass  # stale lock — fall through
        LOCK_FILE.unlink(missing_ok=True)

    LOCK_FILE.write_text(str(os.getpid()))
    typer.echo(f"lock: acquired (PID {os.getpid()})")


def _atomic_write(path: Path, contents: str) -> None:
    """Write via tempfile + os.replace so readers never see a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(contents, encoding="utf-8")
    os.replace(tmp, path)


def _load_seen() -> dict[str, str]:
    if not SEEN_JSON.exists():
        return {}
    return json.loads(SEEN_JSON.read_text())


def _save_seen(seen: dict[str, str]) -> None:
    _atomic_write(SEEN_JSON, json.dumps(seen, indent=2, sort_keys=True))


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


@app.command()
def publish(
    push: bool = typer.Option(False, "--push", help="git push after committing. Default off for safety."),
) -> None:
    """Validate edition.json, update seen.json, commit. Optionally push.

    Hard-fails on schema drift between agent output and EditionJSON. Updates
    state/seen.json (atomic) with any new canonical URLs from this build. Commits
    docs/ + state/. Pushing is gated behind --push so manual smoke tests don't
    accidentally publish."""
    if not EDITION_JSON.exists():
        typer.echo(f"publish: missing {EDITION_JSON}", err=True)
        raise typer.Exit(1)

    edition = EditionJSON.model_validate_json(EDITION_JSON.read_text())
    typer.echo(f"publish: edition.json validates ({len(edition.items)} items)")

    seen = _load_seen()
    new_urls = 0
    now_iso = datetime.now(UTC).isoformat()
    for item in edition.items:
        if item.canonical_url not in seen:
            seen[item.canonical_url] = now_iso
            new_urls += 1
    _save_seen(seen)
    typer.echo(f"publish: seen.json updated (+{new_urls} new URLs, {len(seen)} total)")

    _git("add", "docs/", "state/seen.json")
    if QUESTIONS_MD.exists():
        _git("add", str(QUESTIONS_MD.relative_to(REPO_ROOT)))

    status = _git("status", "--porcelain").stdout.strip()
    if not status:
        typer.echo("publish: nothing to commit")
        LOCK_FILE.unlink(missing_ok=True)
        return

    msg = f"build: edition {edition.built_at.isoformat()} ({len(edition.items)} items)"
    commit_result = _git("commit", "-m", msg, check=False)
    if commit_result.returncode != 0:
        typer.echo(f"publish: commit failed:\n{commit_result.stderr}", err=True)
        raise typer.Exit(1)
    typer.echo(f"publish: committed — {msg}")

    if push:
        push_result = _git("push", check=False)
        if push_result.returncode != 0:
            typer.echo(f"publish: push failed:\n{push_result.stderr}", err=True)
            raise typer.Exit(1)
        typer.echo("publish: pushed")

    LOCK_FILE.unlink(missing_ok=True)
    typer.echo("publish: lock released")


if __name__ == "__main__":
    app()
