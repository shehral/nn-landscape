"""URL + title normalization. Pure functions, no I/O."""

from __future__ import annotations

import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Tracking params we strip from URLs. These never affect content identity.
_TRACKING_PARAMS = frozenset(
    {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_id",
        "fbclid", "gclid", "mc_eid", "mc_cid", "msclkid", "yclid", "_hsenc", "_hsmi",
        "ref", "ref_src", "ref_url", "share", "source",
    }
)

_DEFAULT_PORTS = {"http": "80", "https": "443"}

_WORD_RE = re.compile(r"\w+")
_STOPWORDS = frozenset(
    {
        "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to", "for",
        "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
        "this", "that", "these", "those", "it", "its", "their",
    }
)


def canonical_url(url: str) -> str:
    """Return a canonicalized form so two surface variants of the same page map to one key.

    - Lowercase scheme + host.
    - Drop default port.
    - Drop fragment.
    - Strip well-known tracking parameters; keep + sort the rest.
    - Drop trailing slash from non-root paths.
    """
    parts = urlsplit(url.strip())

    scheme = parts.scheme.lower() or "https"
    host = (parts.hostname or "").lower()
    port = str(parts.port) if parts.port else ""
    if port and _DEFAULT_PORTS.get(scheme) == port:
        port = ""
    netloc = f"{host}:{port}" if port else host

    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    kept_query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k not in _TRACKING_PARAMS]
    kept_query.sort()
    query = urlencode(kept_query)

    return urlunsplit((scheme, netloc, path, query, ""))


def normalize_title(title: str) -> str:
    """Lowercase + Unicode NFKC + whitespace collapse. Stable string for hashing."""
    nfkc = unicodedata.normalize("NFKC", title).casefold()
    return re.sub(r"\s+", " ", nfkc).strip()


def _tokens(text: str) -> set[str]:
    return {t for t in _WORD_RE.findall(text.casefold()) if t not in _STOPWORDS and len(t) > 2}


def jaccard_similarity(a: str, b: str) -> float:
    """Token-level Jaccard. Stopwords + short tokens dropped. Returns 0.0 if both empty."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)
