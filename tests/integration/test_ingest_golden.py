"""Integration tests for ingestion. respx-mocked source fixtures."""

from __future__ import annotations

import httpx
import respx

from landscape.ingest import (
    ArxivSource,
    GitHubTrendingSource,
    HNSource,
    RSSSource,
    run_sources,
)

ARXIV_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2511.05923v1</id>
    <title>Component-resolved causal patching for VLMs</title>
    <summary>We introduce a method for component-resolved patching applied to OCR document tasks and table extraction.</summary>
    <link href="http://arxiv.org/abs/2511.05923v1"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2511.05924v1</id>
    <title>Unrelated reinforcement learning convergence proof</title>
    <summary>A proof of a convergence bound for SARSA.</summary>
    <link href="http://arxiv.org/abs/2511.05924v1"/>
  </entry>
</feed>
"""

HN_FIXTURE = {
    "hits": [
        {"objectID": "100", "title": "Reducto announces $30M Series B for document AI", "url": "https://reducto.ai/blog/series-b", "points": 250},
        {"objectID": "101", "title": "Why some startup folded", "url": "https://example.com/folded", "points": 200},
        {"objectID": "102", "title": "Show HN: vector DB", "url": None, "points": 150},
    ]
}

RSS_FIXTURE = """<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Anthropic News</title>
  <item>
    <title>Claude 4.7 release notes</title>
    <link>https://anthropic.com/news/claude-4-7</link>
  </item>
  <item>
    <title>Research update</title>
    <link>https://anthropic.com/research/update</link>
  </item>
</channel></rss>
"""

GH_FIXTURE = {
    "items": [
        {"full_name": "user/llm-thing", "html_url": "https://github.com/user/llm-thing", "description": "An LLM-related repository."},
        {"full_name": "other/vlm-thing", "html_url": "https://github.com/other/vlm-thing", "description": None},
    ]
}


class TestArxivSource:
    @respx.mock
    def test_keyword_filter(self) -> None:
        respx.get(url__startswith="http://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(200, text=ARXIV_FIXTURE)
        )
        source = ArxivSource(keywords=["OCR", "table"])
        with httpx.Client() as client:
            items = list(source.fetch(client))
        # Only the first entry should match keywords
        assert len(items) == 1
        assert "Component-resolved" in items[0].title
        assert items[0].source == "arxiv"

    @respx.mock
    def test_no_keywords_yields_everything(self) -> None:
        respx.get(url__startswith="http://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(200, text=ARXIV_FIXTURE)
        )
        source = ArxivSource(keywords=[])
        with httpx.Client() as client:
            items = list(source.fetch(client))
        assert len(items) == 2


class TestHNSource:
    @respx.mock
    def test_filters_by_keyword(self) -> None:
        respx.get(url__startswith="https://hn.algolia.com/api/v1/search").mock(
            return_value=httpx.Response(200, json=HN_FIXTURE)
        )
        source = HNSource(keywords=["document"])
        with httpx.Client() as client:
            items = list(source.fetch(client))
        assert len(items) == 1
        assert "Reducto" in items[0].title
        assert items[0].source == "hn"

    @respx.mock
    def test_falls_back_to_hn_item_url_when_external_missing(self) -> None:
        respx.get(url__startswith="https://hn.algolia.com/api/v1/search").mock(
            return_value=httpx.Response(200, json=HN_FIXTURE)
        )
        source = HNSource(keywords=["vector"])
        with httpx.Client() as client:
            items = list(source.fetch(client))
        assert len(items) == 1
        assert items[0].canonical_url.startswith("https://news.ycombinator.com/item")


class TestRSSSource:
    @respx.mock
    def test_parses_feed(self) -> None:
        respx.get("https://anthropic.com/news/rss.xml").mock(
            return_value=httpx.Response(200, text=RSS_FIXTURE)
        )
        source = RSSSource(feeds=["https://anthropic.com/news/rss.xml"])
        with httpx.Client() as client:
            items = list(source.fetch(client))
        assert len(items) == 2
        assert items[0].source == "rss"


class TestGitHubTrendingSource:
    @respx.mock
    def test_yields_repos(self) -> None:
        respx.get(url__startswith="https://api.github.com/search/repositories").mock(
            return_value=httpx.Response(200, json=GH_FIXTURE)
        )
        source = GitHubTrendingSource()
        with httpx.Client() as client:
            items = list(source.fetch(client))
        assert len(items) == 2
        assert items[0].source == "github_trending"
        assert "llm-thing" in items[0].title


class TestRunSourcesIsolation:
    @respx.mock
    def test_failing_source_does_not_kill_others(self) -> None:
        # arxiv 500s; HN responds.
        respx.get(url__startswith="http://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(500, text="server error")
        )
        respx.get(url__startswith="https://hn.algolia.com/api/v1/search").mock(
            return_value=httpx.Response(200, json=HN_FIXTURE)
        )
        sources = [
            ArxivSource(keywords=["OCR"]),
            HNSource(keywords=["document"]),
        ]
        items, failures, covered = run_sources(sources)
        assert len(failures) == 1
        assert failures[0].source == "arxiv"
        assert "hn" in covered
        assert len(items) >= 1
