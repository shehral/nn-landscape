"""Snapshot test for the renderer using syrupy."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml

from landscape.models import (
    AIQuestion,
    AxisScores,
    EditionJSON,
    Framing,
    Item,
    TrendBullet,
)
from landscape.paths import VIEWS_YAML
from landscape.render import render_view


def _fixture_edition() -> EditionJSON:
    items = (
        Item(
            canonical_url="https://arxiv.org/abs/2511.05923",
            title="Component-resolved causal patching for VLMs",
            source="arxiv",
            axis_scores=AxisScores(doc_ai=4, competitive=1, frontier=2, vlm_research=5),
            composite_score=72.0,
            primary_axis="vlm_research",
            secondary_axes=("doc_ai",),
            one_line_summary="Method localizes which transformer components cause the behavior.",
            framing=Framing(
                product_implication="Toolkit for diagnosing Nanonets-OCR2 hallucination modes.",
                research_implication="Applies directly to our phantom-row mitigation work.",
                action_recommendation="Reproduce the smallest experiment within 1 week.",
            ),
        ),
        Item(
            canonical_url="https://reducto.ai/blog/series-b",
            title="Reducto closes $30M Series B",
            source="hn",
            axis_scores=AxisScores(doc_ai=4, competitive=5, frontier=1, vlm_research=1),
            composite_score=68.0,
            primary_axis="competitive",
        ),
    )
    return EditionJSON(
        built_at=datetime(2026, 5, 21, 12, 0, tzinfo=UTC),
        sources_covered=("arxiv", "hn", "rss", "github_trending"),
        items=items,
        trend_bullets=(
            TrendBullet(summary="Two doc-AI startups announced funding this week.", evidence_item_ids=()),
        ),
        ai_partner_questions=(
            AIQuestion(question="Should we weight competitor funding rounds higher?", context="2 rounds this week, none last week."),
        ),
        audit_passed=True,
    )


def test_render_default_view_snapshot(tmp_path: Path, snapshot) -> None:
    edition = _fixture_edition()
    views = yaml.safe_load(VIEWS_YAML.read_text())["views"]
    html = render_view(edition, "default", views["default"], tmp_path / "out.html")
    assert html == snapshot


def test_render_dl_team_view_reweights_scores(tmp_path: Path) -> None:
    """In the dl_team view, vlm_research is weighted 0.40 vs 0.10 for competitive.

    The research item (vlm_research=5) should display a higher score badge than
    the competitive item (vlm_research=1) when rendered for the dl_team audience.
    """
    import re

    edition = _fixture_edition()
    views = yaml.safe_load(VIEWS_YAML.read_text())["views"]
    html = render_view(edition, "dl_team", views["dl_team"], tmp_path / "out.html")

    # Score chips appear inside each item card. Extract pairs of (score, title).
    pattern = re.compile(
        r'<span class="item-score">(\d+)</span>'
        r'.*?<p class="item-title">\s*<a [^>]+>([^<]+)</a>',
        re.DOTALL,
    )
    by_title = {title: int(score) for score, title in pattern.findall(html)}
    research_title = "Component-resolved causal patching for VLMs"
    competitive_title = "Reducto closes $30M Series B"
    assert research_title in by_title
    assert competitive_title in by_title
    assert by_title[research_title] > by_title[competitive_title]
