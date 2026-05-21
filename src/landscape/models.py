"""Pydantic v2 schemas validated at every phase boundary."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

Axis = Literal["doc_ai", "competitive", "frontier", "vlm_research"]
SourceName = Literal["arxiv", "hn", "rss", "github_trending"]

_FROZEN = ConfigDict(frozen=True, extra="forbid")


class AxisScores(BaseModel):
    model_config = _FROZEN

    doc_ai: int
    competitive: int
    frontier: int
    vlm_research: int

    @model_validator(mode="after")
    def _check_ranges(self) -> AxisScores:
        for name, value in self.model_dump().items():
            if not 0 <= value <= 5:
                raise ValueError(f"{name} must be 0..5, got {value}")
        return self


class Framing(BaseModel):
    model_config = _FROZEN

    product_implication: str
    research_implication: str
    action_recommendation: str


class Item(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

    schema_version: int = 1
    id: str = ""
    canonical_url: str
    title: str
    source: SourceName
    source_count: int = 1  # bumped by dedup when same item surfaces from >1 source

    axis_scores: AxisScores | None = None
    composite_score: float | None = None
    primary_axis: Axis | None = None
    secondary_axes: tuple[Axis, ...] = ()
    one_line_summary: str | None = None
    framing: Framing | None = None
    hostility_flag: bool = False

    @model_validator(mode="after")
    def _derive_id(self) -> Item:
        if not self.id:
            digest = hashlib.sha256(self.canonical_url.encode("utf-8")).hexdigest()[:16]
            object.__setattr__(self, "id", digest)
        return self


class TrendBullet(BaseModel):
    model_config = _FROZEN

    summary: str
    evidence_item_ids: tuple[str, ...]


class AIQuestion(BaseModel):
    model_config = _FROZEN

    question: str
    context: str


class SourceFailure(BaseModel):
    model_config = _FROZEN

    source: SourceName
    error: str


class EditionJSON(BaseModel):
    """The agent → renderer contract. Validated at the boundary."""

    model_config = _FROZEN

    schema_version: int = 1
    built_at: datetime
    sources_covered: tuple[SourceName, ...]
    sources_failed: tuple[SourceFailure, ...] = ()
    items: tuple[Item, ...]
    trend_bullets: tuple[TrendBullet, ...] = ()
    ai_partner_questions: tuple[AIQuestion, ...] = ()
    audit_passed: bool
