"""Unit tests for landscape.normalize."""

from __future__ import annotations

import pytest

from landscape.normalize import canonical_url, jaccard_similarity, normalize_title


class TestCanonicalUrl:
    def test_lowercases_scheme_and_host(self) -> None:
        assert canonical_url("HTTPS://Arxiv.ORG/abs/123") == "https://arxiv.org/abs/123"

    def test_drops_fragment(self) -> None:
        assert canonical_url("https://x.com/a#section") == "https://x.com/a"

    def test_strips_tracking_params(self) -> None:
        assert (
            canonical_url("https://x.com/a?utm_source=twitter&utm_campaign=p&q=keep")
            == "https://x.com/a?q=keep"
        )

    def test_drops_default_ports(self) -> None:
        assert canonical_url("http://x.com:80/a") == "http://x.com/a"
        assert canonical_url("https://x.com:443/a") == "https://x.com/a"

    def test_keeps_non_default_ports(self) -> None:
        assert canonical_url("https://x.com:8443/a") == "https://x.com:8443/a"

    def test_drops_trailing_slash_on_non_root(self) -> None:
        assert canonical_url("https://x.com/a/") == "https://x.com/a"

    def test_keeps_root_slash(self) -> None:
        assert canonical_url("https://x.com/") == "https://x.com/"

    def test_sorts_query_params_for_stability(self) -> None:
        a = canonical_url("https://x.com/?b=2&a=1")
        b = canonical_url("https://x.com/?a=1&b=2")
        assert a == b

    def test_two_surface_variants_collapse(self) -> None:
        # The same arXiv paper might appear with several URL shapes.
        variants = [
            "https://arxiv.org/abs/2511.05923",
            "HTTPS://Arxiv.org/abs/2511.05923",
            "https://arxiv.org/abs/2511.05923/",
            "https://arxiv.org/abs/2511.05923?utm_source=hn#abstract",
            "https://arxiv.org:443/abs/2511.05923",
        ]
        canonicalized = {canonical_url(v) for v in variants}
        assert len(canonicalized) == 1


class TestNormalizeTitle:
    def test_lowercases(self) -> None:
        assert normalize_title("Hello World") == "hello world"

    def test_collapses_whitespace(self) -> None:
        assert normalize_title("  hello\n  world  ") == "hello world"

    def test_nfkc_unicode(self) -> None:
        # NFKC normalizes width variants — "ＡＢＣ" (fullwidth) -> "abc"
        assert normalize_title("ＡＢＣ") == "abc"


class TestJaccardSimilarity:
    def test_identical_returns_one(self) -> None:
        s = jaccard_similarity("Component-resolved causal patching", "Component-resolved causal patching")
        assert s == pytest.approx(1.0)

    def test_disjoint_returns_zero(self) -> None:
        s = jaccard_similarity("OCR document layout", "Mistral funding announcement")
        assert s == 0.0

    def test_high_overlap_above_threshold(self) -> None:
        # Same content, slight word-order shuffle
        s = jaccard_similarity(
            "Component-resolved causal patching for VLMs",
            "Component resolved causal patching VLMs",
        )
        assert s >= 0.85

    def test_stopwords_dropped(self) -> None:
        # "the" and short words shouldn't contribute
        a = jaccard_similarity("the cat sat on the mat", "the dog sat on the rug")
        b = jaccard_similarity("cat sat mat", "dog sat rug")
        assert a == pytest.approx(b, rel=0.1)

    def test_both_empty_returns_zero(self) -> None:
        assert jaccard_similarity("", "") == 0.0
