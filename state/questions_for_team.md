# Questions for the team

This file accumulates uncertainty questions raised by the build agent each
cycle. **To reply, append your answer inline below the question.** The
next build's agent reads this file and acts on guidance you have given.

For permanent rule changes (e.g., "we don't care about pricing rounds
under $10M"), edit `data/nanonets_context.md` instead — that's the
agent's editorial grounding.

---

## Build 2026-05-21T08:30:00+00:00 (audit: partial)

### Q: Should NVIDIA Nemotron 3 Nano Omni (item 39c0a1c4f9c26195) be added to the running cross-architecture VLM list for hallucination-transfer experiments?

**Context:** It is explicitly marketed at document agents from a major lab. If yes, it changes the priority of the next reproduction queue; if no, the team should record why so future builds don't re-surface it as a top item.

**Answer:** _add reply here_

### Q: The current source mix is heavily weighted toward newsletters (Latent Space, Interconnects, Import AI, Stratechery, AINews) and frontier-lab blogs; should we add arXiv document-AI feeds and OCR-specific GitHub trending in the next build?

**Context:** This build had 109 of 112 items from RSS and only 3 from HN, with no arXiv or github_trending coverage. The dashboard's value scales with primary-research sources; without them, the doc_ai and vlm_research axes are starved.

**Answer:** _add reply here_

### Q: None of the 112 items names Nanonets directly. Is this expected, or is the keyword filter failing to catch Nanonets-OCR2 mentions?

**Context:** Two consecutive builds without a hostility flag could mean either genuine quiet or a filter miss. A spot-check on HuggingFace and arXiv for 'Nanonets-OCR2' over the last 14 days would resolve this.

**Answer:** _add reply here_

### Q: How should PaddleOCR 3.5 (item 0e90042cc61fe001) be scored on the competitive axis given that PaddleOCR is widely used but not listed in the canonical competitive set in data/nanonets_context.md?

**Context:** It is treated as competitive-axis relevant here because it directly addresses the same workload (OCR + document parsing) as Nanonets-OCR2. Worth confirming whether the editorial grounding should be amended to list PaddleOCR explicitly.

**Answer:** _add reply here_

### Q: Is the score ceiling for an item with no direct Nanonets mention but explicit document-AI positioning correctly tuned? Nemotron 3 Nano Omni and PaddleOCR 3.5 are the two highest-scoring items at ~72 and ~65 respectively.

**Context:** Neither item names Nanonets, but both are direct substitutes / adjacents. If the team would prefer the ceiling around 50 for non-Nanonets-naming items, the rubric or weights need to be retuned in data/nanonets_context.md.

**Answer:** _add reply here_

---

## Build 2026-05-21T08:58:57.842759+00:00 (audit: passed)

### Q: Should Gemini Omni and Nemotron 3 Nano Omni get pre-emptive OmniDocBench and IDP Leaderboard runs before they appear on the published leaderboard, or wait for the team operating the leaderboard to add them?

**Context:** Both arrived this build with explicit multimodal document positioning. Independent runs would give us a private comparator, but duplicating the leaderboard team's work has obvious cost.

**Answer:** _add reply here_

### Q: How should the build separate Google I/O 2026 from the individual Gemini Omni and Gemini 3.5 entries when they cover overlapping material?

**Context:** The roundup item, the Omni release across two URLs, and Gemini 3.5 across two URLs all surface separately because dedup keys on canonical URL. Counting all six inflates the competitive column; collapsing them loses per-axis comparability.

**Answer:** _add reply here_

### Q: Long-context multimodal models claim agent-usable million-token windows; is the implicit framework that document chunking becomes obsolete, or that chunking still wins on cost and accuracy?

**Context:** Nemotron 3 Nano Omni and DeepSeek-V4 both go this direction. The team's existing infrastructure assumes chunked OCR; understanding whether long-context VLMs eat the pipeline or stack on top of it changes roadmap priors.

**Answer:** _add reply here_

### Q: Open-weight VLM releases keep landing without explicit IDP Leaderboard runs; should the dashboard automatically queue a leaderboard submission request for any model that names DocVQA, ChartQA, OmniDocBench or OlmOCR-Bench in its release notes?

**Context:** Manually triggering a benchmark submission for each release is high-overhead; a queue would feed the leaderboard maintainers without the build agent making editorial calls on which model is worth running.

**Answer:** _add reply here_

### Q: arXiv ingestion has been 429-rate-limited for two consecutive builds; should the source path move to a daily ID-list snapshot via OAI-PMH rather than the keyword-search endpoint?

**Context:** The hostility-flag scoring rule depends on academic papers in the mix to function; if arXiv stays unavailable, the dashboard structurally over-weights vendor announcements and undercounts research.

**Answer:** _add reply here_

---

## Build 2026-05-21T12:08:38.941409+00:00 (audit: partial)

### Q: arXiv and HN have returned 403 errors for at least two consecutive builds; should the pipeline switch to a mirror or fallback access path before the next scheduled build?

**Context:** Without arXiv and HN, the doc_ai and vlm_research axes are starved of primary research signal. This build drew 100% of its items from github_trending. The prior build raised the same concern about arXiv rate-limiting; HN 403 is a new regression.

**Answer:** _add reply here_

### Q: opendataloader-pdf is a new open-source PDF parser targeting the same RAG and AI training pipeline use cases as Nanonets Agentic Data Extraction; should it be added to the competitive registry in data/nanonets_context.md?

**Context:** It scored competitive=3 this build and received an 'investigate' recommendation. If the team confirms it is a material entrant, adding it to the competitive set ensures future builds score and frame it correctly from the start.

**Answer:** _add reply here_

### Q: Ollama's description now names GLM-5 as a natively supported model; GLM-OCR is listed in the competitive set but GLM-5 is not — is GLM-5 the same product line or a distinct model that should be added?

**Context:** The two names suggest different products (GLM-5 is a general VLM; GLM-OCR is document-specific). If GLM-5 includes document extraction capabilities comparable to GLM-OCR, it should be in the competitive registry. If not, the scoring on Ollama's GLM-5 mention may be inflated.

**Answer:** _add reply here_

### Q: This build drew entirely from github_trending because arxiv and HN failed; should trend analysis and the framing pass be suppressed or explicitly flagged as 'infrastructure-biased' when fewer than 2 primary research sources contributed?

**Context:** The current signal is weighted entirely toward production tooling (GitHub repos), not research papers. Trends inferred from this mix may not reflect the actual research frontier, and the framing pass lacks the arxiv-based hallucination and VLM internals coverage that grounds the research_implication field.

**Answer:** _add reply here_

### Q: LLaVA-OneVision-1.5 training infrastructure is trending; should the research team actively monitor what document-specific fine-tuned variants are being trained on this base to anticipate new IDP Leaderboard competitive entries?

**Context:** LLaVA-OneVision-based fine-tunes have appeared on the leaderboard in prior builds. A proactive watch on HuggingFace for lmms-eval results on LLaVA-OneVision derivatives would give advance notice before new entries formally submit to the IDP Leaderboard.

**Answer:** _add reply here_

---
