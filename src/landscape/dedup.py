"""Three-function dedup pipeline.

Chained as: group_by_canonical_url -> merge_jaccard_near_duplicates -> apply_source_boost.
Each step is pure and individually testable.
"""

from __future__ import annotations

from collections.abc import Iterable

from .models import Item
from .normalize import jaccard_similarity

JACCARD_THRESHOLD = 0.85
SOURCE_BOOST_MIN = 3  # items present in this many sources or more get the boost


def group_by_canonical_url(items: Iterable[Item]) -> list[Item]:
    """Collapse exact-URL duplicates into one Item with source_count summed."""
    by_url: dict[str, Item] = {}
    for item in items:
        existing = by_url.get(item.canonical_url)
        if existing is None:
            by_url[item.canonical_url] = item
            continue
        by_url[item.canonical_url] = _merge(existing, item)
    return list(by_url.values())


def merge_jaccard_near_duplicates(items: list[Item], threshold: float = JACCARD_THRESHOLD) -> list[Item]:
    """Greedy near-duplicate merge by title Jaccard. O(n^2) — fine for v1 (~150 items/build).

    Keeps the first item from each cluster, sums source_count from cluster members.
    """
    kept: list[Item] = []
    for item in items:
        merged = False
        for i, anchor in enumerate(kept):
            if jaccard_similarity(item.title, anchor.title) >= threshold:
                kept[i] = _merge(anchor, item)
                merged = True
                break
        if not merged:
            kept.append(item)
    return kept


def apply_source_boost(items: list[Item], boost: int = 5, cap: int = 100) -> list[Item]:
    """When composite_score is known, bump items present in >= SOURCE_BOOST_MIN sources.

    Pre-scoring runs (when composite_score is None) are no-ops — boost applied later by
    the scorer or a second pass once scores land.
    """
    out: list[Item] = []
    for item in items:
        if item.composite_score is not None and item.source_count >= SOURCE_BOOST_MIN:
            new_score = min(item.composite_score + boost, cap)
            out.append(item.model_copy(update={"composite_score": new_score}))
        else:
            out.append(item)
    return out


def _merge(a: Item, b: Item) -> Item:
    """Combine two items deemed equivalent. Source_count sums; primary source = a's."""
    return a.model_copy(update={"source_count": a.source_count + b.source_count})
