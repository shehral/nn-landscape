"""Unit tests for Pydantic schemas."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from landscape.models import (
    AIQuestion,
    AxisScores,
    EditionJSON,
    Framing,
    Item,
    SourceFailure,
    TrendBullet,
)


class TestItem:
    def test_id_auto_derived_from_url(self) -> None:
        item = Item(canonical_url="https://arxiv.org/abs/123", title="X", source="arxiv")
        assert len(item.id) == 16
        # Stable: same URL → same id
        same = Item(canonical_url="https://arxiv.org/abs/123", title="Different title", source="hn")
        assert item.id == same.id

    def test_extra_field_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Item(canonical_url="x", title="y", source="arxiv", bogus="z")

    def test_frozen_rejects_mutation(self) -> None:
        item = Item(canonical_url="x", title="y", source="arxiv")
        with pytest.raises(ValidationError):
            item.title = "mutated"

    def test_model_copy_returns_new_instance(self) -> None:
        item = Item(canonical_url="x", title="y", source="arxiv")
        updated = item.model_copy(update={"title": "z"})
        assert item.title == "y"
        assert updated.title == "z"


class TestAxisScores:
    def test_valid_range(self) -> None:
        AxisScores(doc_ai=0, competitive=5, frontier=3, vlm_research=2)

    def test_rejects_above_five(self) -> None:
        with pytest.raises(ValidationError):
            AxisScores(doc_ai=6, competitive=0, frontier=0, vlm_research=0)

    def test_rejects_below_zero(self) -> None:
        with pytest.raises(ValidationError):
            AxisScores(doc_ai=-1, competitive=0, frontier=0, vlm_research=0)


class TestEditionJSON:
    def test_minimal_valid_construction(self) -> None:
        edition = EditionJSON(
            built_at=datetime.now(UTC),
            sources_covered=("arxiv",),
            items=(),
            audit_passed=True,
        )
        assert edition.schema_version == 1
        assert edition.trend_bullets == ()
        assert edition.ai_partner_questions == ()

    def test_round_trip_via_json(self) -> None:
        original = EditionJSON(
            built_at=datetime(2026, 5, 21, 12, 0, tzinfo=UTC),
            sources_covered=("arxiv", "hn"),
            sources_failed=(SourceFailure(source="rss", error="timeout"),),
            items=(Item(canonical_url="https://arxiv.org/abs/1", title="X", source="arxiv"),),
            trend_bullets=(TrendBullet(summary="trend", evidence_item_ids=()),),
            ai_partner_questions=(AIQuestion(question="q?", context="c"),),
            audit_passed=True,
        )
        roundtrip = EditionJSON.model_validate_json(original.model_dump_json())
        assert roundtrip == original

    def test_rejects_unknown_axis_in_item(self) -> None:
        with pytest.raises(ValidationError):
            Item(canonical_url="x", title="y", source="arxiv", primary_axis="invented")

    def test_rejects_unknown_source(self) -> None:
        with pytest.raises(ValidationError):
            Item(canonical_url="x", title="y", source="twitter")


class TestFraming:
    def test_all_three_fields_required(self) -> None:
        with pytest.raises(ValidationError):
            Framing(product_implication="x", research_implication="y")  # type: ignore[call-arg]
