---
name: refresh-nanonets-context
description: Refresh data/nanonets_context.md so the build agent's editorial grounding stays current. Use when scheduled weekly (separate /schedule entry from build-edition) or invoked manually after a known Nanonets release.
---

# refresh-nanonets-context

The build agent's notion of "relevant to Nanonets" is entirely determined
by `data/nanonets_context.md`. If that file goes stale (new flagship
model, new product line, new competitive entrant, deprecated competitor),
the dashboard's scoring degrades silently.

This skill refreshes the context file based on publicly-visible state.
It is intentionally NOT part of build-edition — folding it in would add
20+ web fetches to every cron tick. Run this separately, ideally weekly,
or any time you know something material has changed.

## Recommended schedule

```
/schedule weekly run "claude /skill refresh-nanonets-context" against the shehral/nn-landscape repo
```

Sunday afternoon is fine — quiet news cycle, the refreshed context is
in place for Monday's build.

---

## Steps

### Step 1 — Read the existing context

```
cat data/nanonets_context.md
```

Note the headings: "What Nanonets is", "Active research direction",
"Competitive set (Document AI)", "Frontier-lab signal", "What's
explicitly NOT in this context", "Editorial voice", "When in doubt",
"Last updated". You will preserve this structure.

### Step 2 — Investigate Nanonets' current public posture

In this order:

1. `WebFetch` https://nanonets.com — homepage. Note the products being
   featured. Has the headline product changed? Has positioning shifted?
2. `WebFetch` https://nanonets.com/blog — recent posts (last 30 days).
   Any new model? Any major customer announcement (Fortune-500 type)?
3. `WebSearch` for "site:huggingface.co/nanonets" — list the public
   model artifacts. Any newer than what's in the file?
4. `WebSearch` for "nanonets" arXiv recent. Any team-authored papers?
5. `WebFetch` https://idp-leaderboard.org or benchmarking.nanonets.com
   (whichever resolves) — what's the current #1? Has Nanonets' position
   changed?

### Step 3 — Investigate competitive set freshness

For each named competitor in the existing file, do a quick sanity check:

- `WebSearch` "<competitor name>" 2026 to confirm the company is
  still operating and has not been renamed.
- Note any new entrants you've seen named alongside the existing
  competitors in trade press.

Specifically watch for:
- New OCR-VLM models from the Asian model labs (Qwen, GLM, DeepSeek,
  Kimi, Tencent, Baidu) that target document AI.
- New entrants in the document-API space (e.g., a new YC batch
  document-AI startup, a major-cloud-provider's new endpoint).
- Frontier labs shipping document-specific tooling on their main
  product surface.

### Step 4 — Investigate frontier-lab document signal

The file has a strict frontier-vs-competitive disambiguation rule. Check
whether the named examples in that section are still current:

- `WebSearch` "Gemini document mode" — is this still the marketing
  name? Has it been renamed or deprecated?
- Same for OpenAI's vision-for-docs offering (whatever it's currently
  called) and Anthropic's document-extraction tooling.

If a named example has been renamed or deprecated, update it.

### Step 5 — Update the file

Apply the changes. Constraints:

- **Public-safe only.** The file is public. No internal strategy, no
  customer names, no internal-team priorities.
- **Conservative on edits.** If you can't confirm a fact from a public
  source you trust, leave the current text alone. Update only what
  you have evidence for.
- **Preserve structure.** Same section headings. Same voice
  (analyst-grade, no hype). Same disambiguation rules.
- **Always update the trailing "Last updated" section.** Add an entry
  with today's date, the sources you consulted, and a short list of
  what changed.

### Step 6 — Commit + push

```
git add data/nanonets_context.md
git commit -m "chore: refresh Nanonets context from public sources"
git push
```

That's the entire output. The next `/build-edition` cron tick will pick
up the new grounding.

---

## What this skill does NOT do

- Run the dashboard build (that's `/skill build-edition`).
- Modify sources.yaml or views.yaml (those are tuning the *system*,
  not the *grounding*).
- Add internal-only context (forbidden by the file's own rules).
- Reach out to the Nanonets team for clarification (this skill is
  observe-only — record what's public, don't ask).

## Failure modes

- **Nanonets-related websites are down or unreachable.** Abort cleanly;
  do not edit the file. A stale context is better than a guessed one.
- **You can't confirm a previously-listed competitor still exists.**
  Leave them in the file with a note in the Last-Updated section that
  manual verification is warranted. Don't silently delete.
- **You found a new flagship model but the file already references it.**
  No change needed; just record the verification in Last-Updated.

## How the team replies

The team replies via `data/nanonets_context.md` edits directly (this is
where editorial policy lives) or via the AI-partner-channel reply flow
on the rendered dashboard (`state/questions_for_team.md`). This refresh
skill is one-way — it reads public state into the file, not from the
team back.
