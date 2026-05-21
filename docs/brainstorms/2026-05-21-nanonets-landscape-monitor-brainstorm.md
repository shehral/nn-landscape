# Brainstorm — Nanonets AI/Research Landscape Monitor

**Date:** 2026-05-21
**Owner:** Shehral Ali
**Audience for the artifact:** Prathamesh Juvatkar (CTO), Nanonets DL team, plus public-shareable
**Status:** Brainstorm complete, ready for `/ce:plan`

---

## What We're Building

A **continuously-updated, public-shareable web dashboard** that aggregates
and ranks AI/ML news, papers, blogs, and other artifacts from the open web —
filtered and scored for **strategic relevance to Nanonets**. The goal is to
give Prathamesh and the Nanonets DL team daily visibility into the moving
parts of the AI / Doc-AI landscape and help them build the right *taste* and
*intuition* about where the field is going.

**It is explicitly not a feed reader.** Every surfaced item carries a
relevance score and a structured editorial annotation framed in
Nanonets-specific terms. The product is *curated intelligence*, not raw
aggregation.

### Working name (placeholder)
`Nanonets Landscape` — final name TBD with the team.

---

## Architecture — Claude-Agents-As-Pipeline

The pipeline is not a Python service. It is a **scheduled remote Claude Code
agent** that runs a project skill, modifies the repo, commits, and pushes.
GitHub Pages serves the rendered output. There is no FastAPI worker, no
Postgres, no Vercel project — just this repo and a `/schedule` entry.

```
┌──────────────────────────────────────────────────────────────────┐
│  /schedule → remote Claude Code agent (every 6 hours)            │
│  invokes the `build-edition` project skill                       │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  .claude/skills/build-edition/                                   │
│    1. Reads data/nanonets_context.md  (relevance grounding)      │
│    2. Reads data/sources.yaml         (source list + filters)    │
│    3. For each source: WebFetch / arXiv API / HN Algolia / RSS   │
│    4. Scores, frames, writes structured per-item JSON            │
│    5. Cross-item trend detection pass                            │
│    6. Renders index.html + editions/<date>.html + per-audience   │
│       views (for-prathamesh.html, for-dl-team.html)              │
│    7. Commits + pushes                                           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  GitHub Pages serves /docs from this repo                        │
│  Public URL: https://<user>.github.io/agentic-extraction-...     │
│  (custom domain later, e.g. landscape.nanonets.com)              │
└──────────────────────────────────────────────────────────────────┘
```

### Why this architecture
- No infra to babysit. No API key management beyond what the remote agent
  needs (a GitHub PAT to push commits).
- The agent IS the editorial mind. One model does ingestion + scoring +
  framing + trend detection in a single coherent pass — coherence comes for
  free instead of being stitched together across Haiku + Opus + Python.
- Plain-English maintenance. Add a source? Edit `data/sources.yaml`. Retune
  what relevance means? Edit `data/nanonets_context.md`.
- Meta-on-brand. The Nanonets landscape monitor is itself built by AI agents
  on a cron — appropriate framing for a Nanonets Applied-AI-Research artifact.

### Known properties (not bugs)
- **Lower determinism than a hand-coded pipeline.** Each run's scoring can
  drift run-to-run. For an editorial product this is fine — taste isn't
  deterministic. Document on the About page.
- **Source coverage is bounded by what an agent can reach via WebFetch / public
  APIs.** No X / Twitter in v1 (no paid scraping path); Substack roundups
  (AINews, Latent Space) cover X discourse adequately.
- **Cost model is "remote agent minutes," not API tokens.** A full build
  likely takes 5–15 min of agent compute; 4 runs/day ≈ 30–60 min/day. Worth
  confirming `/schedule` billing before locking the cadence.

---

## Key Decisions

### Decision 1 — Content axes (weighted)
Items are scored across four axes; weighting reflects the team's stated
priority order:

| Axis | Weight | Why |
|---|---|---|
| **Document AI / OCR / structured extraction** | 0.35 | Core business. Mistral OCR, Reducto, Unstructured.io, Anthropic / Google / OpenAI vision moves for docs, layout-aware models, table-extraction research, dataset releases. |
| **Competitive + business intelligence** | 0.30 | Prathamesh-facing. Funding, customer wins, pricing, hiring signals, enterprise-AI adoption signals from competitors and adjacent players. |
| **Frontier LLM / lab signals** | 0.20 | Strategic context. OpenAI / Anthropic / Google DeepMind / Meta releases, capability evals, scaling and efficiency news, agent-platform moves. |
| **VLM research (hallucinations, mech interp)** | 0.15 | Directly feeds the team's research output. Qwen-VL, InternVL, Phi-VL, LLaVA, multimodal hallucination papers, VLM circuits. |

Composite score = weighted sum, normalized to 0–100.

### Decision 2 — Source set
Six source classes, all reachable from a remote Claude Code agent:
1. **arXiv** — `cs.CV`, `cs.CL`, `cs.LG`, `cs.AI` with keyword filters
   (OCR, document, VLM, hallucination, layout, table, extraction).
2. **Hacker News** — Algolia API top stories with score ≥ 100 OR keyword
   match.
3. **Bluesky** — public API; hand-curated DL / Doc-AI list of ~50 accounts.
4. **Curated RSS blogs** — ~30 hand-picked feeds (Anthropic, OpenAI, Google
   DeepMind, Mistral, Reducto, Unstructured, Mendable, LangChain, Together,
   Hugging Face, Cohere, Databricks, AssemblyAI, etc.).
5. **GitHub trending** — repos filtered by language + topic + recency,
   re-ranked by Nanonets-context match.
6. **Substacks** — Stratechery, Latent Space, Interconnects, AINews,
   Import AI, The Information. These also serve as the X-discourse proxy in
   v1 (no direct X coverage; deferred indefinitely).

### Decision 3 — Scoring + framing (single agent pass)
The remote agent does everything in one workflow:
1. **Ingest** — pull items from each source class.
2. **Pre-filter** — drop items that don't keyword-match or topic-match the
   Nanonets context. Cheap; done by the agent inline.
3. **Score** — for each surviving item, emit JSON with 0–5 scores on each
   axis plus a 1-line summary.
4. **Frame (top-20 only)** — write structured 2-3-sentence annotations:
   - *Implication for Nanonets product:*
   - *Implication for Nanonets research:*
   - *Action / no action this week:*
5. **Trend pass** — over the full day's surfaced items, produce a
   "patterns I'm seeing this week" section (3-5 bullets).
6. **AI-partner channel** — flag items the agent is uncertain about, ask
   clarifying questions about Nanonets strategy, or push back on framing.
   Surfaces under a "Questions for the team" sidebar.

### Decision 4 — Audience-tagged views
Three rendered surfaces from the same scored data:
- `index.html` — default view, weights as in Decision 1.
- `for-prathamesh.html` — competitive (0.40) + frontier (0.30) + Doc-AI
  (0.20) + research (0.10). Strategic skew.
- `for-dl-team.html` — research (0.40) + Doc-AI (0.30) + frontier (0.20) +
  competitive (0.10). Technical skew.

All three deploy from the same build. Toggle in UI: simple top-nav links.

### Decision 5 — Repo layout
```
agentic-extraction-landscape/
  .claude/
    skills/
      build-edition.md          # the main agent skill
  data/
    nanonets_context.md         # editorial grounding (versioned in-repo)
    sources.yaml                # source list + filters
  docs/                         # GitHub Pages root
    index.html                  # latest edition (default view)
    for-prathamesh.html
    for-dl-team.html
    editions/
      2026-05-21-1200.html      # archived editions, timestamped
    assets/
      styles.css                # tailwind-derived; static, no build step
  state/
    last_build.json             # build timestamp, item hashes, dedup
    questions_for_team.md       # accumulating AI-partner channel
  README.md
  docs/brainstorms/             # design history
```

GitHub Pages source: `docs/` folder on `main`.

### Decision 6 — Nanonets-context bundle composition
The `data/nanonets_context.md` v1 includes:
- **Product lines + current research focus** — Nanonets-OCR2-3B, OCR3 (not
  touched in current work), the document-VLM stack, customer-facing
  extraction APIs, and the active research line: *VLM hallucinations broadly*
  (phantom rows, repetition loops, infinite generation as subtypes).
- **Named competitive set** — Mistral OCR, Reducto, Unstructured.io,
  Mendable, Docling, Tesseract, plus Anthropic / Google / OpenAI vision-for-docs
  offerings.

Explicitly *not* in the public-shareable context bundle (privacy /
strategic-disclosure reasons):
- Internal paper-submission targets.
- Per-stakeholder strategic priorities.
- Internal roadmap.

If/when a team-only private surface is built, those go there instead.

### Decision 7 — Editorial voice
- Analyst-grade, terse, no hype, no emoji, no marketing copy.
- Reference points: Stratechery (framing), The Information (sourcing),
  Interconnects (technical posture).
- Default item card displays: [score · axis · source · timestamp] · headline
  · 1-line summary · (top-20 only) structured 3-line framing.

### Decision 8 — Schedule + cost guardrails
- Build cadence: **every 6 hours** via `/schedule` (e.g., 06:00, 12:00,
  18:00, 00:00 PT).
- Per-build time budget: ≤ 20 minutes of agent compute.
- Per-build hard ceiling: stop and commit partial output if budget exceeded.
- Manual-trigger path: `claude /skill build-edition` runnable locally for
  debugging without waiting on the cron.

---

## v1 Deliverable (ship-by-tomorrow morning)

- [ ] Repo scaffolded with the layout above.
- [ ] `data/nanonets_context.md` v1 written with the two approved categories.
- [ ] `data/sources.yaml` populated with all six source classes.
- [ ] `.claude/skills/build-edition.md` implemented end-to-end.
- [ ] One real edition built locally — `docs/index.html` + the two
      audience-tagged views + one archived edition.
- [ ] GitHub Pages enabled, public URL live.
- [ ] `/schedule` configured to run `build-edition` every 6 hours.
- [ ] README explains: what this is, how it's built (the meta story),
      how to retune the context bundle, how to add sources.
- [ ] About page on the dashboard linking to the repo and explaining
      "built by Claude Code agents on a 6-hour cron."

---

## v2 / future (not in scope tomorrow)

- Custom domain (`landscape.nanonets.com`) after Prathamesh signs off on
  v1 format.
- "New since you last viewed" markers (cookie-based; no auth).
- Team-only private surface for sensitive strategic notes.
- Personalization per team-member interest profile.
- Direct X / Twitter coverage if a paid path becomes available.
- Migration to a Next.js dashboard with live re-ranking, if v1's static
  every-6-hours cadence proves insufficient.

---

## Open Questions (none block overnight build)

1. **`/schedule` billing model** — confirm whether scheduled remote-agent
   minutes are metered separately or included in plan. Run one build
   manually first to estimate per-run time before activating the cron.
2. **Public-vs-gated for competitive intel** — for v1, everything is public
   and the context bundle excludes internal strategy. Revisit if any item's
   framing feels too sensitive to ship publicly.
3. **Final name + URL** — `Nanonets Landscape` placeholder; revisit after
   Prathamesh sees v1.
4. **Source-attribution etiquette for paid Substacks** — default to
   link-only with 1-line summary, no body excerpt. Revisit if any source
   pushes back.

---

## Success Criteria

**Tomorrow morning (post overnight build):**
- [ ] Live public URL renders today's edition.
- [ ] Real items from all six source classes are present.
- [ ] Each item has a real score and 1-line summary; top-20 have the
      structured 3-line framing (product / research / action).
- [ ] Cross-item trend pass produces 3-5 bullets on the day.
- [ ] AI-partner channel has at least one item flagged.
- [ ] Two audience-tagged views work.
- [ ] Build is reproducible — `claude /skill build-edition` re-runs cleanly.

**Week-2:**
- [ ] Scheduled cron has run unattended for ≥ 5 cycles.
- [ ] Prathamesh has seen the dashboard and given format feedback;
      at least one round of edits incorporated.

**Strategic (Q3 2026):**
- [ ] Dashboard becomes a recurring artifact in Tuesday / Thursday team
      check-ins — links replace ad-hoc "did you see this paper?" Slack
      messages.
- [ ] At least one edition seeds an internal blog or research direction
      conversation.

---

## Out of Scope (YAGNI)

- Per-user accounts / auth.
- Mobile-native app.
- Push notifications.
- Multi-language support.
- ML-trained ranking (LLM-as-judge inside the agent is sufficient).
- Internal Slack / Linear / Notion integrations.

---

## Next Step

Run `/ce:plan` against this brainstorm to produce the overnight
implementation plan. The plan should sequence tasks so an unattended
overnight session can ship v1 by morning.
