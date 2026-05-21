---
title: Nanonets AI Landscape Monitor — Agents-as-Pipeline Dashboard
type: feat
status: active
date: 2026-05-21
origin: docs/brainstorms/2026-05-21-nanonets-landscape-monitor-brainstorm.md
---

# Nanonets AI Landscape Monitor — Agents-as-Pipeline Dashboard

## Overview

A scheduled remote Claude Code agent runs every 6 hours, ingests AI/ML
artifacts from the open web via a small Python package, scores and frames
the survivors against a Nanonets-specific editorial context, and commits
regenerated HTML to this repo. GitHub Pages serves the result at a public
URL. Three audience-tagged views (default, `for-prathamesh.html`,
`for-dl-team.html`) render from the same scored data using a single
template with per-audience weights.

This plan ships a working v1 overnight (≈5 hours of focused work) and
sequences a v1.x evolution over the following two weeks. Revised after
technical review by architecture-strategist, kieran-python-reviewer, and
code-simplicity-reviewer.

## Problem Statement / Motivation

Prathamesh (Nanonets CTO) and the Nanonets DL team currently parse the AI
landscape ad-hoc. Building *taste* — knowing what's worth attention vs.
noise — requires an editorial filter, not a raw aggregator.

The team-owned production metric is **papers, blogs, and benchmarks
published** (see global CLAUDE.md). A landscape monitor that surfaces
high-relevance items and forces structured "implication for product /
research / action" framing is itself a publishable artifact that
contributes to that metric — and it compounds by feeding Tuesday/Thursday
DL-team check-ins and Wednesday 1:1 prep.

(See brainstorm: `docs/brainstorms/2026-05-21-nanonets-landscape-monitor-brainstorm.md`
for the WHAT and WHY in full.)

## Proposed Solution

**Hybrid: deterministic Python at the edges, agent reasoning in the middle,
deterministic Python at the edges again.** The agent never directly touches
state-of-truth files — it consumes typed inputs and emits typed proposals
that Python ratifies.

### Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  /schedule (cron, every 6h)                                          │
│      │                                                               │
│      ▼                                                               │
│  Remote Claude Code agent                                            │
│      │ reads .claude/skills/build-edition/SKILL.md (the playbook)    │
│      │                                                               │
│      │  shell:  python -m landscape.cli ingest                       │
│      │           → state/run/items_raw.jsonl                         │
│      │                                                               │
│      │  shell:  python -m landscape.cli dedup                        │
│      │           → state/run/items_deduped.jsonl                     │
│      │                                                               │
│      │  agent:  scoring (Haiku subagent over deduped, in batches)    │
│      │           → state/run/items_scored.jsonl                      │
│      │                                                               │
│      │  agent:  framing (Sonnet for top-N), trend pass, AI-partner   │
│      │           → state/run/edition.json  (Pydantic-validated)      │
│      │                                                               │
│      │  shell:  python -m landscape.cli render                       │
│      │           → docs/index.html, docs/for-*.html, docs/about.html │
│      │                                                               │
│      │  shell:  python -m landscape.cli publish                      │
│      │           — checklist gate, update state/seen.json,           │
│      │             commit, push                                      │
│      ▼                                                               │
│  GitHub Pages serves docs/ on push                                   │
└──────────────────────────────────────────────────────────────────────┘
```

The agent is the editorial mind. The CLI commands are deterministic
infrastructure. SKILL.md is the playbook + editorial guide — it does NOT
hold control flow as untyped markdown.

### Repo layout

```
agentic-extraction-landscape/
├── .claude/
│   └── skills/
│       └── build-edition/
│           └── SKILL.md             # editorial guide + playbook (not control flow)
├── data/
│   ├── nanonets_context.md          # editorial grounding (public-safe)
│   ├── sources.yaml                 # source list + filters
│   └── views.yaml                   # per-audience weight configurations
├── src/
│   └── landscape/
│       ├── __init__.py
│       ├── models.py                # Pydantic v2: Item, EditionJSON, …
│       ├── paths.py                 # centralized path constants
│       ├── normalize.py             # URL + title normalization
│       ├── ingest.py                # Source protocol + 4 sources + run_sources()
│       ├── dedup.py                 # 3-function pipeline
│       ├── render.py                # Jinja2 renderer
│       └── cli.py                   # CLI entry points (typer or argparse)
├── templates/
│   ├── edition.html.j2              # one template, audience param
│   ├── about.html.j2
│   └── partials/
│       ├── item_card.html.j2
│       ├── trend_block.html.j2
│       └── ai_partner_block.html.j2
├── docs/                            # GitHub Pages root
│   ├── .nojekyll
│   ├── robots.txt                   # noindex until sign-off
│   ├── index.html
│   ├── for-prathamesh.html
│   ├── for-dl-team.html
│   ├── about.html
│   ├── assets/styles.css
│   ├── brainstorms/                 # (already exists)
│   └── plans/                       # (already exists)
├── state/
│   ├── seen.json                    # {canonical_url: first_seen_iso}
│   ├── questions_for_team.md        # AI-partner channel accumulator
│   ├── .lock                        # concurrent-build guard
│   └── run/                         # per-build working files (gitignored)
├── tests/
│   ├── unit/
│   │   ├── test_normalize.py
│   │   ├── test_dedup.py
│   │   └── test_models.py
│   └── integration/
│       ├── test_ingest_golden.py    # respx-mocked source fixtures
│       └── test_render_snapshot.py  # syrupy snapshots
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

### Item schema (frozen, Pydantic v2)

```python
# src/landscape/models.py
from pydantic import BaseModel, ConfigDict
from typing import Literal

Axis = Literal["doc_ai", "competitive", "frontier", "vlm_research"]

class AxisScores(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    doc_ai: int            # 0-5
    competitive: int
    frontier: int
    vlm_research: int

class Framing(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    product_implication: str
    research_implication: str
    action_recommendation: str

class Item(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    schema_version: int = 1
    id: str                          # sha256(canonical_url)[:16]
    canonical_url: str
    title: str
    source: Literal["arxiv", "hn", "rss", "github_trending"]
    axis_scores: AxisScores | None = None
    composite_score: float | None = None
    primary_axis: Axis | None = None
    secondary_axes: list[Axis] = []   # SpecFlow C2: multi-axis items
    one_line_summary: str | None = None
    framing: Framing | None = None
    hostility_flag: bool = False      # SpecFlow C4: load-bearing
```

11 fields. `schema_version` lets future schema changes coexist without
backfill. Optional fields are None until the relevant phase populates them.

### EditionJSON schema (the agent → render contract)

```python
class TrendBullet(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    summary: str
    evidence_item_ids: list[str]

class AIQuestion(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    question: str
    context: str

class EditionJSON(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    schema_version: int = 1
    built_at: datetime
    sources_covered: list[str]
    items: list[Item]
    trend_bullets: list[TrendBullet]
    ai_partner_questions: list[AIQuestion]
    audit_passed: bool
```

The agent emits `state/run/edition.json` which is validated against this
schema before render. Drift between agent output and renderer input is
impossible.

## Implementation Phases

### Phase A — Local end-to-end with stub scoring (≈2.5 h)

Build the entire pipeline minus the agent. Produces a real-looking HTML
edition driven by stub scoring, so render quality can be tuned without
burning agent tokens.

**Deliverables:**
1. `pyproject.toml` (uv-managed): `feedparser`, `httpx`, `jinja2`,
   `pydantic`, `pyyaml`, `pytest`, `respx`, `syrupy`, `typer`. No
   `python-dateutil` (stdlib `fromisoformat` suffices in 3.11+).
2. `src/landscape/models.py` — Item, EditionJSON, AxisScores, Framing.
3. `src/landscape/paths.py` — centralized path constants for every state /
   data / docs / template file. Future v2 swaps storage by editing one file.
4. `src/landscape/normalize.py` — `canonical_url()` (strip UTM, lowercase
   host, drop trailing slash, drop fragment), `normalize_title()`,
   `jaccard_similarity()`.
5. `src/landscape/ingest.py`:
   - `class Source(Protocol)` with `name: str` and
     `fetch(client: httpx.Client) -> Iterable[Item]`.
   - Four source classes: `ArxivSource`, `HNSource`, `RSSSource`,
     `GitHubTrendingSource`. Each ≤ 60 lines.
   - `run_sources(sources, timeout=90) -> tuple[list[Item], list[SourceFailure]]`
     owns all try/except + timeout + coverage manifest. One central place.
6. `src/landscape/dedup.py` — three pure functions chained:
   - `group_by_canonical_url(items)` → groups identical URLs.
   - `merge_jaccard_near_duplicates(groups, threshold=0.85)` → titles.
   - `apply_source_boost(merged, boost=5, cap=100)` → 3+ sources → +5 to
     composite (when composite is set; otherwise a flag for the scorer).
7. `src/landscape/render.py` — Jinja2 environment + `render_edition(edition,
   audience)`; one template `edition.html.j2`, audience-aware via a
   weights dict from `data/views.yaml`.
8. `src/landscape/cli.py` — typer commands: `ingest`, `dedup`, `render`,
   `publish`, `build` (orchestrates all).
9. `data/sources.yaml` v1: arXiv (cs.CV+cs.CL+cs.LG+cs.AI w/ keyword
   filter), HN (Algolia, points≥100 last 24h + keywords), RSS (10
   feeds — Anthropic, OpenAI, DeepMind, Mistral, Hugging Face, Latent
   Space, Interconnects, AINews, Stratechery, Import AI), GitHub trending
   (AI/ML repos last 24h).
10. `data/nanonets_context.md` v1 (public-safe): product lines + active
    research line (VLM hallucinations broadly), named competitive set.
    Explicit exclusions: internal paper-submission targets, per-stakeholder
    priorities, internal roadmap.
11. `data/views.yaml` — three audiences, each a Dict[axis, weight].
12. Templates: `edition.html.j2`, `about.html.j2`, three partials.
    Inline Tailwind-derived CSS in `docs/assets/styles.css` (no build
    step). Carry typography conventions from `~/nn-infinite-gen/code/build_report.py`.
13. `docs/about.html` content drafted: meta story, coverage gaps
    (no X/Discord/private-Slack — SpecFlow F2), attribution policy
    (link-only + ≤25-word summary + `nofollow` outbound — SpecFlow H3),
    "not a Nanonets-corporate statement" disclaimer (SpecFlow H4),
    takedown contact.
14. `docs/robots.txt`: `User-agent: *\nDisallow: /` (lift after sign-off
    — SpecFlow H4).
15. `tests/unit/test_normalize.py`, `test_dedup.py`, `test_models.py`.
16. `tests/integration/test_ingest_golden.py` (respx-mocked source
    fixtures), `test_render_snapshot.py` (syrupy snapshots).
17. **Stub scoring** — `cli.py build --stub` populates random-but-deterministic
    scores so renderer can be exercised. Run end-to-end locally; open
    `docs/index.html` in browser; iterate on typography/layout until it
    looks publishable.

**Exit criterion:** `python -m landscape.cli build --stub` produces three
HTML views from real ingested items + stub scores, all tests green.

### Phase B — Agent integration (≈1.5 h)

Wire the real LLM-driven scoring and framing.

**Deliverables:**
1. `.claude/skills/build-edition/SKILL.md` — playbook the remote agent
   reads. Contents:
   - High-level steps (run `landscape.cli ingest`, then `dedup`, then
     score these JSONL records, then frame top-N, then trend pass, then
     AI-partner pass, then `landscape.cli render`, then `landscape.cli
     publish`).
   - Editorial guidance: voice, tone, anti-patterns.
   - Inline 3-5 exemplar framings (SpecFlow F1; reviewers wanted to
     inline rather than separate file).
   - Hostile-content handling instructions (SpecFlow C4): if an item
     mentions Nanonets by name in a critical context, set `hostility_flag=true`,
     use neutral-framing template ("how the competitor positions this"),
     route to `questions_for_team.md` not public top-N.
   - Pre-publish Y/N checklist (5 questions, agent answers inline; if any
     "no," skip publish and append to `questions_for_team.md`).
2. `src/landscape/cli.py publish` subcommand: validates
   `state/run/edition.json` against `EditionJSON` schema (rejects on
   drift), copies items into `state/seen.json` with timestamps, runs
   `git add docs/ state/seen.json state/questions_for_team.md`, commits
   with structured message (`build: edition <timestamp>`), pushes.
3. `state/.lock` convention: `cli.py build` writes a lock file with PID
   on entry; another build process aborts if `.lock` exists and PID is
   alive. Removes on exit/crash via signal handler.
4. End-to-end real-agent build run manually via `claude /skill
   build-edition` once. Inspect token cost; expect ≤ $3.
5. Iterate prompts: if any axis is consistently under-populated, tune
   exemplars; if framing reads bland, tighten voice instructions in SKILL.md.

**Exit criterion:** one real, published-locally edition with all three
views, real scores, real framing, trend bullets, AI-partner questions.

### Phase C — GitHub + Pages + /schedule (≈1 h)

**Deliverables:**
1. `gh repo create shehral/agentic-extraction-landscape --public --source=.`
2. Push.
3. Enable GitHub Pages on `main` / `/docs`:
   `gh api repos/shehral/agentic-extraction-landscape/pages --method POST
   --field source.branch=main --field source.path=/docs`
4. Verify public URL serves; verify `robots.txt` blocks crawling.
5. Add `<meta http-equiv="cache-control" content="max-age=300">` and a
   visible `built_at` timestamp to each rendered page (SpecFlow F4).
6. Run `/schedule` to fire `build-edition` every 6 hours
   (00:00, 06:00, 12:00, 18:00 PT). Confirm telemetry.
7. Tail logs through first 2 cron-fired builds; verify pushes land
   cleanly.

**Exit criterion:** first cron-fired build of v1 is live on GitHub Pages,
all three views serve correctly, robots.txt blocks indexing.

## Alternative Approaches Considered

| Approach | Why rejected |
|---|---|
| Pure-Python pipeline (FastAPI + Postgres + Vercel) | Brainstorm Approach A. Too much infra; `/schedule` strictly simpler. |
| Pure-agent (agent WebFetches everything) | Burns agent time on HTTP work httpx does cheaper. |
| Editorial-first, automation later (brainstorm Approach C) | User wants live dashboard by morning. |
| Daily-only cadence | User asked for 6h cadence; matches strategic-intel use case. |
| Append-only items.jsonl history store | First draft of this plan had it. Removed: cross-edition history isn't needed for v1's use cases (trend pass operates on current build; "what's new" handled by `seen.json`). Cut ~150 LOC. |
| Atomic `_build/` swap publishing | Removed: GH Pages caches 5min, traffic is low, half-built window is sub-second locally. Render direct to `docs/`. |
| Three template files (one per audience) | Collapsed to one template with weights dict; eliminates drift between views. |

## System-Wide Impact

### Interaction Graph

`/schedule` cron → remote agent → SKILL.md playbook → 4 CLI commands +
3 agent reasoning steps → git push → GH Pages async serve. Each CLI
command is contractually defined by Pydantic models at its inputs and
outputs; the agent reasoning steps emit `edition.json` validated against
`EditionJSON`. There is **no shared mutable state across phases** — each
phase reads from versioned files in `state/run/` and writes new ones.

### Error & Failure Propagation

- Per-source ingest failure: caught in `run_sources()`, surfaced in
  `sources_covered` list, build continues. ≥3-of-4 sources required to
  proceed; otherwise abort.
- Dedup or render failure: abort with non-zero exit; agent surfaces in
  `questions_for_team.md`; existing `docs/` remains untouched (last good
  edition serves).
- Agent reasoning step failure: agent retries the failing batch up to
  2×, then commits partial framing only for items that completed BOTH
  scoring and framing (Architecture's recommendation — partials never
  reach `seen.json`).
- Publish failure (e.g., push rejected): the build commit stays local;
  next build re-pushes if `git status` shows ahead.

### State Lifecycle Risks

- `state/seen.json` is a flat `{canonical_url: first_seen_iso}` map.
  Write-replace each build (atomic on POSIX via tempfile + rename).
  No append-only complexity.
- `state/.lock` prevents concurrent builds corrupting `seen.json`.
- `state/run/*.jsonl` are per-build ephemeral working files, gitignored,
  rotated each build.
- `state/questions_for_team.md` is append-only, one section per build,
  capped at ~50 entries with oldest pruned (Simplicity's "won't exceed
  50KB in a month" observation — fine for v1).

### API Surface Parity

Three rendered views from the same Items + EditionJSON:
- `index.html` — default weights (Doc-AI 0.35, competitive 0.30,
  frontier 0.20, research 0.15).
- `for-prathamesh.html` — competitive 0.40 + frontier 0.30 + Doc-AI
  0.20 + research 0.10.
- `for-dl-team.html` — research 0.40 + Doc-AI 0.30 + frontier 0.20 +
  competitive 0.10.

Re-weighting at render time, NOT re-scoring (per SpecFlow + Architecture
agreement). Weights live in `data/views.yaml` so v2 (Next.js) can read
the same config.

### Integration Test Scenarios

1. **Source outage**: arXiv returns 503 → `sources_covered: [hn, rss,
   github_trending]`, build proceeds with banner; test asserts
   `audit_passed=True` if ≥3 sources, `False` otherwise.
2. **Hostile item**: Reducto blog "Why Nanonets is wrong about
   layout-aware OCR" → `hostility_flag=true` → routed to neutral framing
   → surfaces in `questions_for_team.md`, not in top-N of public view.
3. **Cross-source dup**: Same arXiv paper appears via arXiv + HN +
   Latent Space within 24h → one Item in EditionJSON, source-boost +5,
   three source citations.
4. **Partial agent crash**: Haiku scoring crashes after 80/100 items →
   only 80 enter `state/run/items_scored.jsonl`; framing pass only runs
   on those 80; `seen.json` only gains URLs that completed both scoring
   and framing.
5. **Concurrent build**: Manual `claude /skill build-edition` fires
   while `/schedule` build is mid-flight → `.lock` blocks the manual
   one with a clear error message.

## Acceptance Criteria

### Functional Requirements
- [ ] `src/landscape/` package builds with `uv sync`; all imports work.
- [ ] All four v1 source adapters fetch real items in `python -m
      landscape.cli ingest`.
- [ ] Dedup contract implemented as 3-function pipeline; canonical URL
      primary, Jaccard ≥ 0.85 fallback, source-merge boost +5 (capped 100).
- [ ] Item + EditionJSON Pydantic schemas validate at every phase
      boundary; mismatches fail loudly.
- [ ] SKILL.md drives end-to-end build via the agent; `edition.json`
      passes `EditionJSON.model_validate_json()`.
- [ ] Renderer produces three audience-tagged views + about page from
      `data/views.yaml` weights.
- [ ] About page covers attribution policy, coverage gaps, "not a
      corporate statement" disclaimer, takedown contact.
- [ ] `robots.txt` ships with `Disallow: /` until Prathamesh approves v1.
- [ ] `/schedule` configured every 6h; `.lock` prevents concurrent runs.

### Non-Functional Requirements
- [ ] Per-build agent token cost ≤ $3.
- [ ] Per-build wall-clock ≤ 20 min (including HTTP fetches).
- [ ] First contentful paint of `index.html` ≤ 1.5 s on cold cache.
- [ ] Mobile-responsive at ≥ 360 px.
- [ ] No hard-coded secrets in repo.

### Quality Gates
- [ ] Unit tests (normalize, dedup, models) green.
- [ ] Integration tests (ingest golden, render snapshot) green.
- [ ] Manual review of the first 3 editions before flipping
      `robots.txt`.
- [ ] No emoji in editorial content (per brainstorm Decision 7).

## Success Metrics

**Tomorrow morning:**
- Live (but `noindex`) edition rendering from all four source classes.
- Each top-N item has the structured 3-line framing.
- Trend block + AI-partner channel both populated.
- All tests green; cost ≤ $3.

**Week-1:**
- ≥ 24 successful unattended cron builds.
- Prathamesh has reviewed v1; at least one round of format edits
  incorporated; `robots.txt` flipped to allow indexing.

**Week-4:**
- Dashboard referenced in ≥ 2 DL-team check-ins; one edition seeds an
  internal blog or paper direction (counts toward the team-owned papers/
  blogs/benchmarks metric).

## Dependencies & Prerequisites

- Python ≥ 3.11, `uv`.
- Libraries (in `pyproject.toml`): `feedparser`, `httpx`, `jinja2`,
  `pydantic >= 2.6`, `pyyaml`, `pytest`, `respx`, `syrupy`, `typer`.
- `gh` CLI authenticated for repo creation + Pages enable.
- `/schedule` skill operational (cost model validated in Phase B).
- Anthropic API access for the remote agent.
- A public GitHub repo under Shehral's account.

## Risk Analysis & Mitigation

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | `/schedule` billing higher than expected | M | M | Manual single build in Phase B measures cost before activation. |
| R2 | Editorial blandness; framing reads generic | M | H | Inline exemplar framings in SKILL.md; Sonnet (not Haiku) for framing; manual review of first 3 editions. |
| R3 | Source format brittleness (RSS, GH HTML scrape) | H | L | Per-source try/except in `run_sources()`; coverage in `sources_covered`. |
| R4 | Hostile-content embarrassment on public page | L | H | `hostility_flag` field, neutral-framing template, routing to `questions_for_team.md`; `robots.txt` until approved. |
| R5 | Copyright / paywall ethics on Substacks | L | H | Link-only + ≤25-word summary + `nofollow` outbound; takedown contact in About. |
| R6 | First-edition quality is "meh"; team unimpressed | M | M | `robots.txt noindex` until sign-off; iterate privately first 48h. |
| R7 | Misattribution as Nanonets-corporate statement | M | H | About-page disclaimer; `noindex` until approved. |
| R8 | Concurrent build corrupts state | L | M | `state/.lock` file prevents. |
| R9 | Schema drift between agent output and renderer | M | M | Pydantic `EditionJSON` validates at boundary; mismatches fail loudly. |

## Resource Requirements

- Active engineering: ≈5 hours (one focused overnight session).
- Per-build runtime cost: target ≤ $3, 4 builds/day → ≤ $12/day. Validate
  Phase B.
- Storage: < 10 MB for first month (no items.jsonl history; just
  `seen.json` + `questions_for_team.md`).
- Domains/hosting: GitHub free tier only.

## Future Considerations

- **v1.1**: Bluesky integration via `data/bluesky_accounts.yaml` + public
  `bsky.app` API.
- **v1.2**: items.jsonl content-addressed history store (re-introduced
  when freshness checks or cross-edition trend tracking become needed).
- **v1.3**: Custom domain `landscape.nanonets.com` post-sign-off.
- **v1.4**: "What's new since last visit" via cookie markers.
- **v2**: Next.js dashboard with live re-ranking if 6-hour static
  cadence is insufficient. `data/views.yaml` + `landscape/render.py`
  port cleanly because weights and rendering logic are already
  config-driven.
- **v2.x**: Per-team-member interest profile; email digest; team-only
  surface; X coverage if a paid path becomes available.

## Documentation Plan

- `README.md`: project meta story, local-dev setup, how to retune
  context bundle, how to add sources, how to disable `/schedule`.
- `docs/about.html`: public — coverage gaps, attribution policy,
  disclaimer, takedown contact, build provenance.
- `state/questions_for_team.md`: lives at the repo root, updated each
  build, reviewed in Tuesday/Thursday check-ins.

## Sources & References

### Origin
- **Brainstorm**: [`docs/brainstorms/2026-05-21-nanonets-landscape-monitor-brainstorm.md`](../brainstorms/2026-05-21-nanonets-landscape-monitor-brainstorm.md)
  — key decisions carried: agents-as-pipeline architecture, four-axis
  weighted scoring, audience-tagged views, no direct X coverage,
  public-safe context bundle.

### Internal patterns reused
- `~/nn-infinite-gen/code/build_report.py` — self-contained HTML
  typography conventions, "Questions from your AI partner" pattern,
  provenance footer.

### Technical review incorporated
- **Architecture reviewer** — Pydantic at every phase boundary,
  `state/.lock`, `schema_version` field, `data/views.yaml`, SKILL.md
  demoted to playbook with Python orchestrator via CLI commands.
- **Kieran (Python conventions)** — `src/landscape/` proper package,
  Pydantic v2 frozen models, `Source` protocol, dedup as 3-function
  pipeline, sync httpx, tests split unit/integration with respx + syrupy,
  drop `python-dateutil`.
- **Simplicity reviewer** — drop items.jsonl content-addressed store
  (use `seen.json`), drop atomic swap (render direct to `docs/`), one
  template + audience weights (not three template files), inline
  exemplar framings, defer circuit breaker and editions archive, slim
  Item schema to 11 fields, three phases not seven.

### SpecFlow analysis incorporated
- Dedup contract (C1) → 3-function pipeline + 14-day source-merge logic.
- Multi-axis items (C2) → `secondary_axes` field retained.
- Partial-build recovery (C3) → handled via "only complete-pipeline
  items reach seen.json" (no atomic swap needed once partial commits
  are forbidden).
- Hostile content (C4) → `hostility_flag` + neutral-framing template.
- Source outages (H1) → `sources_covered` + per-source try/except.
- Stale content (H2) → freshness check deferred (no items history in
  v1); revisit in v1.2.
- Copyright/paywall (H3) → attribution policy in About.
- Misattribution (H4) → disclaimer + `noindex` until approved.
- Framing drift (F1) → inline exemplar framings in SKILL.md.
- X-gap visibility (F2) → About-page coverage gaps section.
- Commit storms (F3) → circuit breaker deferred (3-streak failure over
  18h not a v1 concern; address if observed).
- CDN cache (F4) → cache-control meta + visible `built_at` timestamp.

### External references
- arXiv export API: `export.arxiv.org/api/query`.
- HN Algolia API: `hn.algolia.com/api/v1/search`.
- GitHub Pages serve from `/docs` on `main`.
- Anthropic Claude Code skills format — verify with
  `mcp__plugin_compound-engineering_context7__query-docs` in Phase B
  before finalizing SKILL.md frontmatter.
