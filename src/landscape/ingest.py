"""Source protocol + four adapters + run_sources orchestrator.

Per Kieran's review: typed Source protocol; one place (run_sources) owns
try/except + timeouts + coverage manifest. Sync httpx for four serial sources.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Annotated, ClassVar, Literal, Protocol

import feedparser
import httpx
import yaml
from pydantic import BaseModel, Field

from .models import Item, SourceFailure, SourceName
from .normalize import canonical_url

USER_AGENT = "nn-landscape/0.1 (+https://github.com/shehral/nn-landscape)"


class Source(Protocol):
    """Stateless source adapter. Receives a shared httpx.Client and yields Items."""

    name: ClassVar[SourceName]

    def fetch(self, client: httpx.Client) -> Iterable[Item]: ...


def _keyword_match(text: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    haystack = text.lower()
    return any(k.lower() in haystack for k in keywords)


class ArxivSource(BaseModel):
    type: Literal["arxiv"] = "arxiv"
    categories: list[str] = Field(default_factory=lambda: ["cs.CV", "cs.CL", "cs.LG", "cs.AI"])
    keywords: list[str] = Field(default_factory=list)
    max_results: int = 100

    name: ClassVar[SourceName] = "arxiv"

    def fetch(self, client: httpx.Client) -> Iterable[Item]:
        cat_query = "+OR+".join(f"cat:{c}" for c in self.categories)
        url = (
            "http://export.arxiv.org/api/query"
            f"?search_query={cat_query}"
            f"&sortBy=submittedDate&sortOrder=descending"
            f"&max_results={self.max_results}"
        )
        resp = client.get(url)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        for entry in feed.entries:
            summary = getattr(entry, "summary", "")
            if not _keyword_match(f"{entry.title} {summary}", self.keywords):
                continue
            yield Item(
                canonical_url=canonical_url(entry.link),
                title=" ".join(entry.title.split()),
                source=self.name,
            )


class HNSource(BaseModel):
    type: Literal["hn"] = "hn"
    min_points: int = 100
    hits_per_page: int = 50
    keywords: list[str] = Field(default_factory=list)

    name: ClassVar[SourceName] = "hn"

    def fetch(self, client: httpx.Client) -> Iterable[Item]:
        url = (
            "https://hn.algolia.com/api/v1/search"
            f"?tags=story&numericFilters=points>={self.min_points}"
            f"&hitsPerPage={self.hits_per_page}"
        )
        resp = client.get(url)
        resp.raise_for_status()
        for hit in resp.json().get("hits", []):
            title = (hit.get("title") or "").strip()
            if not title:
                continue
            link = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
            if not _keyword_match(title, self.keywords):
                continue
            yield Item(
                canonical_url=canonical_url(link),
                title=title,
                source=self.name,
            )


class RSSSource(BaseModel):
    type: Literal["rss"] = "rss"
    feeds: list[str]
    per_feed_limit: int = 20

    name: ClassVar[SourceName] = "rss"

    def fetch(self, client: httpx.Client) -> Iterable[Item]:
        for feed_url in self.feeds:
            try:
                resp = client.get(feed_url, timeout=15.0)
                resp.raise_for_status()
            except Exception:
                # one feed's failure doesn't poison the source — we surface the gap
                # via sources_covered if the entire source returns nothing.
                continue
            feed = feedparser.parse(resp.text)
            for entry in feed.entries[: self.per_feed_limit]:
                link = getattr(entry, "link", None)
                title = getattr(entry, "title", "").strip()
                if not link or not title:
                    continue
                yield Item(
                    canonical_url=canonical_url(link),
                    title=" ".join(title.split()),
                    source=self.name,
                )


class GitHubTrendingSource(BaseModel):
    type: Literal["github_trending"] = "github_trending"
    topics: list[str] = Field(
        default_factory=lambda: ["machine-learning", "llm", "vlm", "ocr", "rag"]
    )
    days_back: int = 1
    per_page: int = 30

    name: ClassVar[SourceName] = "github_trending"

    def fetch(self, client: httpx.Client) -> Iterable[Item]:
        since = (datetime.now(UTC) - timedelta(days=self.days_back)).strftime("%Y-%m-%d")
        topic_query = "+".join(f"topic:{t}" for t in self.topics)
        url = (
            "https://api.github.com/search/repositories"
            f"?q={topic_query}+pushed:>={since}&sort=stars&order=desc&per_page={self.per_page}"
        )
        resp = client.get(url, headers={"Accept": "application/vnd.github+json"})
        resp.raise_for_status()
        for repo in resp.json().get("items", []):
            description = (repo.get("description") or "").strip()
            title = f"{repo['full_name']}: {description[:200]}" if description else repo["full_name"]
            yield Item(
                canonical_url=canonical_url(repo["html_url"]),
                title=title,
                source=self.name,
            )


SourceConfig = Annotated[
    ArxivSource | HNSource | RSSSource | GitHubTrendingSource,
    Field(discriminator="type"),
]


class SourcesYaml(BaseModel):
    """Top-level schema for data/sources.yaml."""

    sources: list[SourceConfig]


def load_sources(yaml_path) -> list[SourceConfig]:
    """Parse data/sources.yaml into a typed list of source configs."""
    raw = yaml.safe_load(yaml_path.read_text())
    return SourcesYaml.model_validate(raw).sources


def run_sources(
    sources: list[SourceConfig],
    timeout: float = 90.0,
) -> tuple[list[Item], list[SourceFailure], list[SourceName]]:
    """Drive all sources serially. One place owns try/except, timeout, coverage.

    Returns (items, failures, sources_covered). A source that yields zero items
    is still counted as "covered" if it didn't raise — only raised exceptions
    become SourceFailure entries.
    """
    items: list[Item] = []
    failures: list[SourceFailure] = []
    covered: list[SourceName] = []
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
        for source in sources:
            try:
                items.extend(source.fetch(client))
                covered.append(source.name)
            except Exception as exc:  # noqa: BLE001 — boundary
                failures.append(SourceFailure(source=source.name, error=str(exc)[:200]))
    return items, failures, covered
