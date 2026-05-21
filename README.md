# Nanonets AI Landscape Monitor

A continuously-updated, public-shareable dashboard that aggregates and ranks
AI/ML news, papers, blogs, and other artifacts from the open web, filtered
and scored for **strategic relevance to Nanonets**.

The dashboard is **built by Claude Code agents on a 6-hour cron**. Every six
hours a scheduled remote agent ingests items from arXiv, Hacker News,
curated RSS, and GitHub trending; scores them on four axes (Document AI,
Competitive, Frontier, VLM research); writes a 3-line "Implication for
product / research / action" framing for the top items; surfaces emerging
patterns and AI-partner questions; and commits the regenerated HTML.
GitHub Pages serves the result.

## Architecture

```
/schedule cron (every 6h) → remote Claude Code agent
  → reads .claude/skills/build-edition/SKILL.md (the playbook)
  → python -m landscape.cli ingest      (HTTP fetch, no LLM)
  → python -m landscape.cli dedup       (canonical URL + Jaccard fallback)
  → agent: score (Haiku subagent)       (LLM judgment)
  → agent: frame top-N + trend pass + AI-partner pass (LLM judgment)
  → python -m landscape.cli render      (Jinja2 → HTML)
  → python -m landscape.cli publish     (validate, commit, push)
→ GitHub Pages serves docs/
```

The agent is the editorial mind. Python at the edges. Pydantic models
validate every phase boundary.

## Local development

Requires Python ≥ 3.11 and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
python -m landscape.cli build --stub
open docs/index.html
```

The `--stub` flag uses deterministic synthetic scoring so the renderer can
be exercised without burning agent tokens.

## Re-tuning relevance

The agent's notion of "relevant to Nanonets" lives entirely in
[`data/nanonets_context.md`](data/nanonets_context.md). To shift what gets
surfaced or how it's framed, edit that file and commit. The next build
will use the new context.

## Adding sources

Edit [`data/sources.yaml`](data/sources.yaml). For new RSS feeds, just add
to the list. For new source types (e.g., Bluesky), add a new class in
`src/landscape/ingest.py` implementing the `Source` protocol.

## Layout

```
agentic-extraction-landscape/
├── .claude/skills/build-edition/   # agent playbook + editorial guide
├── data/                            # context bundle, sources, weights
├── src/landscape/                   # the package
├── templates/                       # Jinja2 templates
├── docs/                            # GitHub Pages root (rendered HTML)
├── state/                           # seen.json + questions_for_team.md
└── tests/                           # unit + integration
```

## Documentation

- [`docs/about.html`](docs/about.html) — public-facing: coverage gaps,
  attribution policy, disclaimers, build provenance.
- [`docs/brainstorms/`](docs/brainstorms/) — design history.
- [`docs/plans/`](docs/plans/) — implementation plans.
- [`state/questions_for_team.md`](state/questions_for_team.md) — the AI
  agent's accumulating questions for the team.

## Status

v1 in active development. Indexing is currently disabled
(`docs/robots.txt`: `Disallow: /`) until the editorial format is reviewed
and approved.

## License

Internal Nanonets project. License TBD on public release.
