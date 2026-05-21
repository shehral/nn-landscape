"""Unit tests for the 3-function dedup pipeline."""

from __future__ import annotations

from landscape.dedup import (
    apply_source_boost,
    group_by_canonical_url,
    merge_jaccard_near_duplicates,
)
from landscape.models import Item


def _item(url: str, title: str, source: str = "arxiv", source_count: int = 1) -> Item:
    return Item(canonical_url=url, title=title, source=source, source_count=source_count)


class TestGroupByCanonicalUrl:
    def test_distinct_urls_pass_through(self) -> None:
        items = [_item("a", "A"), _item("b", "B"), _item("c", "C")]
        out = group_by_canonical_url(items)
        assert len(out) == 3

    def test_duplicate_urls_merge(self) -> None:
        items = [_item("a", "A", "arxiv"), _item("a", "A", "hn")]
        out = group_by_canonical_url(items)
        assert len(out) == 1
        assert out[0].source_count == 2

    def test_preexisting_source_counts_sum(self) -> None:
        items = [
            _item("a", "A", "arxiv", source_count=2),
            _item("a", "A", "hn", source_count=3),
        ]
        out = group_by_canonical_url(items)
        assert out[0].source_count == 5


class TestMergeJaccardNearDuplicates:
    def test_low_similarity_kept_separate(self) -> None:
        items = [_item("a", "OCR document layout"), _item("b", "Mistral funding round")]
        out = merge_jaccard_near_duplicates(items)
        assert len(out) == 2

    def test_high_similarity_merged(self) -> None:
        items = [
            _item("a", "Component-resolved causal patching for VLMs"),
            _item("b", "Component resolved causal patching VLMs"),
        ]
        out = merge_jaccard_near_duplicates(items, threshold=0.85)
        assert len(out) == 1
        assert out[0].source_count == 2

    def test_anchor_is_first_seen(self) -> None:
        items = [
            _item("a", "Component-resolved causal patching for VLMs", "arxiv"),
            _item("b", "Component resolved causal patching VLMs", "hn"),
        ]
        out = merge_jaccard_near_duplicates(items)
        # The first item's URL and source are kept as the canonical representation.
        assert out[0].canonical_url == "a"
        assert out[0].source == "arxiv"


class TestApplySourceBoost:
    def test_noop_when_composite_score_absent(self) -> None:
        items = [_item("a", "A", source_count=5)]
        out = apply_source_boost(items)
        assert out == items

    def test_under_threshold_unchanged(self) -> None:
        item = _item("a", "A", source_count=2).model_copy(update={"composite_score": 70.0})
        out = apply_source_boost([item])
        assert out[0].composite_score == 70.0

    def test_boost_applied_at_threshold(self) -> None:
        item = _item("a", "A", source_count=3).model_copy(update={"composite_score": 70.0})
        out = apply_source_boost([item])
        assert out[0].composite_score == 75.0

    def test_boost_capped(self) -> None:
        item = _item("a", "A", source_count=3).model_copy(update={"composite_score": 98.0})
        out = apply_source_boost([item], boost=5, cap=100)
        assert out[0].composite_score == 100.0
