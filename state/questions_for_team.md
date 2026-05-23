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

## Build 2026-05-21T18:12:27+00:00 (audit: partial)

### Q: MinerU has appeared at the top of the competitive axis across multiple consecutive builds; should it be added to the named competitive set in data/nanonets_context.md alongside Reducto, LlamaParse, and Unstructured.io?

**Context:** MinerU is backed by Shanghai AI Lab (opendatalab), targets the PDF and Office document-to-markdown/JSON extraction interface that Nanonets Agentic Data Extraction occupies, and consistently scores composite=68 — highest item in the build. Without a named entry, future builds evaluate it without pre-established axis weights that would sharpen scoring.

**Answer:** _add reply here_

### Q: BiSheng and RAGFlow both address the enterprise document orchestration layer that Nanonets Agents also occupies; are either of these tracked commercially, and should they be added to the competitive set in data/nanonets_context.md?

**Context:** Both are open-source, Chinese-backed (DataElement and Infiniflow respectively), and have appeared in multiple consecutive builds. They operate above the extraction layer — pipeline orchestrators rather than OCR models — which makes them a different threat profile than Reducto or MinerU. Clarifying whether they belong in the registry would stabilize scoring.

**Answer:** _add reply here_

### Q: Ollama's description now lists Kimi-K2.5 (Moonshot AI) alongside GLM-5 and Qwen; should Moonshot AI or Kimi-K2.5 be added to the competitive or frontier tracking set in data/nanonets_context.md?

**Context:** Moonshot AI is not currently in the editorial grounding. Kimi-K2.5 appears to be a multimodal model; if it includes document extraction capabilities comparable to GLM-OCR or Qwen-VL, it belongs in the competitive registry. If it is a general multimodal model without document focus, it would be frontier-primary. The build cannot resolve this without team input.

**Answer:** _add reply here_

### Q: Two open-source evaluation frameworks (lmms-eval, evalscope) are now trending that cover DocVQA, ChartQA, and IDP Leaderboard-adjacent benchmarks; is either already in use by the team for benchmark runs, or does the team use a custom harness?

**Context:** If the team uses neither and maintains a custom evaluation infrastructure, that gap is worth noting to avoid redundant investment. If one is already in use, these items should be promoted to a higher action recommendation in future builds and the context file updated to reflect that.

**Answer:** _add reply here_

### Q: The trend toward open-source document-parsing commoditization (MinerU, opendataloader-pdf, and the already-listed Docling) is now visible across three consecutive builds; should data/nanonets_context.md be updated to include a paragraph on open-source substitution risk in the competitive section?

**Context:** Docling is the only open-source parser currently named in the competitive registry. MinerU and opendataloader-pdf represent a second and third entrant in the same category. A context-level note on this class of entrants would stabilize scoring across builds without requiring the build agent to make ad hoc judgments about whether each new open-source PDF parser belongs in the competitive axis.

**Answer:** _add reply here_

---

## Build 2026-05-22T00:17:49+00:00 (audit: partial)

### Q: GLM-5 and Kimi-K2.5 have appeared in the Ollama description for multiple consecutive builds; should the IDP Leaderboard team run benchmark evaluations on GLM-5 before deciding whether to add it to the competitive registry alongside GLM-OCR?

**Context:** Prior builds raised whether GLM-5 is distinct from GLM-OCR or a general VLM. No team answer has arrived. If GLM-5 has document extraction capabilities comparable to GLM-OCR, it and Kimi-K2.5 should be named in data/nanonets_context.md; without this, the Ollama item is scored on inference rather than confirmed fact.

**Answer:** _add reply here_

### Q: Should the dashboard render a structural 'infrastructure-biased build' warning when fewer than 2 primary research sources (arxiv, HN) contributed, distinct from the existing partial-build banner?

**Context:** The partial-build banner fires when fewer than 3 of 4 sources succeed, but does not distinguish between losing a newsletter (RSS) and losing arXiv. Four consecutive builds with no arXiv or HN means the vlm_research and doc_ai research_implication fields are being inferred from GitHub repos rather than papers, which changes the epistemic status of the framing.

**Answer:** _add reply here_

### Q: opendataloader-pdf has appeared in two consecutive builds with an 'investigate' recommendation; has the team checked whether it is a material competitive entrant warranting addition to data/nanonets_context.md?

**Context:** It targets the same PDF-to-AI-ready-output interface as the Nanonets Agentic Data Extraction /parse endpoint and is open-source. Without a named entry in the competitive registry, future builds re-evaluate it from scratch each time rather than tracking it as a known entrant.

**Answer:** _add reply here_

### Q: PaperBanana (llmsresearch/paperbanana) automates academic figure and diagram extraction; should it be tracked as research infrastructure relevant to the team's academic paper consumption workflow?

**Context:** Google Research's PaperBanana extracts figures from papers programmatically. An open-source implementation now trending on GitHub suggests growing adoption. If the team consumes academic figures manually today, this could reduce that overhead — but the team is the only one who knows whether that workflow exists.

**Answer:** _add reply here_

---

## Build 2026-05-22T06:07:17+00:00 (audit: partial)

### Q: lmms-eval and evalscope are both trending with overlapping benchmark coverage (DocVQA, ChartQA, IDP-adjacent tasks); which, if either, does the team use for internal OCR-3 benchmark runs, and does OCR-3 appear in either framework's model registry?

**Context:** Confirming internal usage would change these items from 'monitor' to a higher-priority integration action; if neither is used, the team should evaluate one before a competitor uses it to publish a head-to-head benchmark against OCR-3.

**Answer:** _add reply here_

### Q: The self-reflective hallucination-aware multimodal RAG approach uses retrieval-side mitigation rather than mechanistic interpretability; does the research team track this paradigm separately, and are the two approaches evaluated on the same benchmarks so results are comparable?

**Context:** If both paradigms are active in the literature but only one is being pursued internally, the team may be missing an opportunity to use retrieval-based mitigation as a cheap baseline or ablation against the interpretability work.

**Answer:** _add reply here_

### Q: RAGFlow has appeared for multiple consecutive builds as an enterprise document orchestration competitor; should it be added to the competitive registry in data/nanonets_context.md alongside Dify as an 'above-extraction-layer' competitor to Nanonets Agents?

**Context:** Both are open-source, target enterprise document workflows, and have different threat profiles than extraction-layer competitors like MinerU or Reducto. A named registry entry would stabilize scoring across builds without the agent making ad hoc judgments each time.

**Answer:** _add reply here_

### Q: ms-swift now explicitly supports GRPO training for Qwen3-VL and GLM-5.1; has the team assessed the likelihood that GRPO-fine-tuned document VLM variants will appear on the IDP Leaderboard within the next 1-2 build cycles?

**Context:** GRPO has produced SOTA improvements on reasoning tasks; if applied to document VLMs, it could narrow the gap to OCR-3. Early awareness would allow the team to prepare benchmark baselines before a new entry lands on the leaderboard.

**Answer:** _add reply here_

### Q: arxiv and HN have returned 403 errors for five or more consecutive builds; has the team investigated whether the failures are network policy, IP blocking, or rate limiting, and is there an alternative access path such as the arXiv OAI-PMH endpoint or the HN Firebase API?

**Context:** Without arxiv and HN, the vlm_research and doc_ai axes are sourced entirely from GitHub trending repos, which skews the dashboard toward tooling and away from primary research. This build is the fifth consecutive infrastructure-biased build with no arXiv or HN coverage.

**Answer:** _add reply here_

---

## Build 2026-05-22T10:20:00+00:00 (audit: partial)

### Q: MinerU has appeared at the top of the competitive axis for multiple consecutive builds without a team response; should it be added to the named competitive set in data/nanonets_context.md, and if so, with what description and axis weights?

**Context:** Without a registry entry, each build re-evaluates MinerU from first principles. It targets the same PDF-to-markdown/JSON extraction interface as Nanonets Agentic Data Extraction, is backed by Shanghai AI Lab (opendatalab), and consistently scores composite=65 — the highest item in this build.

**Answer:** _add reply here_

### Q: Both lmms-eval and evalscope are now trending with benchmark coverage that includes DocVQA and ChartQA; does the team use either for internal OCR-3 benchmark runs, and does OCR-3 appear in either framework's model registry?

**Context:** If neither is used internally, a competitor could publish a credible head-to-head comparison using one or both before the team has an established rebuttal baseline. The prior question from build 2026-05-22T06:07:17 remains unanswered.

**Answer:** _add reply here_

### Q: arXiv and HN have returned 403 errors for seven consecutive builds; has the team investigated whether the failures are network policy, IP blocking, or rate limiting, and is there an action plan for the OAI-PMH or HN Firebase API alternatives?

**Context:** The pipeline is now structurally limited to github_trending, which skews coverage toward production tooling and away from primary research. Prior builds have surfaced this; no team action has been confirmed. Each build without arXiv degrades the vlm_research and doc_ai axes' epistemic reliability.

**Answer:** _add reply here_

### Q: opendataloader-pdf has appeared in three consecutive builds with an 'investigate' recommendation; has the team checked whether it warrants addition to data/nanonets_context.md as a named competitive entrant?

**Context:** It targets the same /parse interface as Nanonets Agentic Data Extraction and is open-source. Without a registry entry, future builds re-evaluate it from scratch rather than tracking it as a known entrant alongside MinerU and Docling.

**Answer:** _add reply here_

### Q: Should the dashboard render a distinct infrastructure-biased build warning when fewer than 2 primary research sources (arXiv, HN) contribute, distinct from the existing partial-build banner?

**Context:** The partial-build banner fires for any source count below 3 but does not distinguish between losing a newsletter and losing arXiv. Seven consecutive builds without arXiv changes the epistemic status of the vlm_research and doc_ai framing fields in a way the current banner does not communicate.

**Answer:** _add reply here_

---

## Build 2026-05-22T18:17:11+00:00 (audit: partial)

### Q: UltraRAG (OpenBMB) uses the Model Context Protocol to build RAG pipelines; is the Nanonets Agentic Data Extraction API MCP-compatible, or is this a distribution gap that could be addressed to improve developer reach via MCP-native toolchains?

**Context:** MCP has emerged as a standard integration protocol for AI toolchains. If Nanonets lacks an MCP connector, it may be absent from pipelines where developers default to MCP-native parsers, ceding that distribution channel to open-source alternatives like MinerU or opendataloader-pdf.

**Answer:** _add reply here_

### Q: Two retrieval-based multimodal hallucination mitigation projects appeared this build; should the research team formally benchmark a retrieval-side approach on the phantom-row task to establish whether it complements or is redundant to the mechanistic interpretability line?

**Context:** If retrieval-based mitigation achieves comparable phantom-row reduction at lower engineering cost, it could accelerate the production mitigation path while the interpretability work continues. The prior build asked whether the team tracks this paradigm — that question remains unanswered.

**Answer:** _add reply here_

### Q: Paperless-ngx (community-supported DMS for scanning, indexing, archiving) is consistently trending; its user base targets the same document volumes as Nanonets' SME accounts. Is there an integration story where the Nanonets API serves as the AI extraction layer inside paperless-ngx or similar self-hosted DMS workflows?

**Context:** A paperless-ngx plugin or documented integration would reach a community of self-hosted document management users without paid acquisition cost. The overlap in target document types (receipts, invoices, forms) makes this a natural fit for the Nanonets /parse or /extract endpoint.

**Answer:** _add reply here_

### Q: This is the ninth or more consecutive build in which arXiv and HN have been unavailable; should the team add Semantic Scholar or Papers With Code to data/sources.yaml as alternative academic paper sources while the arXiv network issue persists?

**Context:** Semantic Scholar provides an open, rate-limit-friendly API with the same arXiv paper metadata; Papers With Code links papers to code and benchmarks. Either would partially restore the doc_ai and vlm_research research signal. Prior builds have surfaced the arXiv 403 issue repeatedly with no team action confirmed.

**Answer:** _add reply here_

---

## Build 2026-05-23T00:15:01+00:00 (audit: partial)

### Q: Should Dify be added to the competitive registry in data/nanonets_context.md as an above-extraction-layer agentic workflow competitor to Nanonets Agents?

**Context:** Dify is a production-ready agentic workflow platform with document processing capabilities that has appeared in multiple consecutive builds at composite=36. It is not currently named in the competitive registry. Classifying it consistently with BiSheng and RAGFlow (both pending registry-inclusion questions) would stabilize scoring and avoid per-build ad hoc judgments. Prior builds have not asked specifically about Dify.

**Answer:** _add reply here_

### Q: Should OCR-3 be submitted to the lmms-eval and/or evalscope model registries so it appears in third-party benchmark publications using these toolkits?

**Context:** lmms-eval and evalscope are both trending and cover DocVQA, ChartQA, and IDP-adjacent benchmarks. Without OCR-3 in either framework's model registry, competitors publishing via these toolkits will present comparisons that structurally omit OCR-3. Prior builds asked whether the team uses these frameworks internally; this question is about external-facing registry visibility, which is a distinct publishing decision.

**Answer:** _add reply here_

### Q: Should SGLang be evaluated as a serving infrastructure candidate for OCR-3, given its explicit multimodal model support and high-throughput design for large VLMs?

**Context:** SGLang is trending as a high-performance multimodal serving framework. OCR-3 is a 35B MoE model; serving at scale carries concrete per-token costs that an optimized framework could reduce. Confirming whether the team already uses an equivalent solution would allow the dashboard to score SGLang as either infrastructure-relevant or not applicable in future builds, rather than flagging it each time it trends.

**Answer:** _add reply here_

### Q: Is there a distribution risk where enterprise customers adopt RAGFlow, BiSheng, or Dify and use their bundled open-source parsers (Unstructured.io, opendataloader-pdf) by default, bypassing Nanonets Agentic Data Extraction entirely?

**Context:** This build shows the extraction-layer (Unstructured, opendataloader-pdf) and orchestration-layer (RAGFlow, BiSheng, Dify) open-source ecosystems both trending simultaneously. If orchestration platforms integrate open-source parsers by default, Nanonets loses the parsing tier when customers select full-stack open-source toolchains. The prior builds have tracked each of these individually; this question asks about the combined distribution dynamic.

**Answer:** _add reply here_

---

## Build 2026-05-23T06:08:35+00:00 (audit: partial)

### Q: Dify, BiSheng, and RAGFlow all trend simultaneously this build; does Nanonets Agentic Data Extraction have native connectors in any of these three platforms, and if not, is building one a prioritized distribution task?

**Context:** All three are production-ready open-source document workflow platforms that bundle their own parsing defaults. Without native connectors, Nanonets is absent from the default extraction choice for developers who adopt these orchestration platforms, and each build that shows them trending without a connector represents a growing gap.

**Answer:** _add reply here_

### Q: Does the team have a quantitative accuracy threshold — on DocVQA, OmniDocBench, or the IDP Leaderboard — below which the gap between OCR-3 and open-source alternatives becomes a key retention risk argument for enterprise customers?

**Context:** The open-source stack (Unstructured, opendataloader-pdf, evalscope, ms-swift) now covers every stage of the document AI pipeline. Framing the make-vs-buy question around a specific accuracy differential would allow the dashboard to flag when a competitor crosses the threshold rather than tracking individual releases in isolation.

**Answer:** _add reply here_

### Q: ms-swift now supports GRPO fine-tuning for IDP Leaderboard-proximate models (Qwen3-VL, GLM-5.1, InternVL3.5). At what benchmark performance level on OmniDocBench or DocVQA would the team consider a GRPO-fine-tuned open-weight model a material threat to OCR-3's IDP Leaderboard position?

**Context:** GRPO has produced SOTA improvements on reasoning tasks; applied to document VLMs via an accessible toolchain (ms-swift), it could narrow the gap to OCR-3 on extraction accuracy. Early awareness of an incoming GRPO submission would allow the team to prepare benchmark baselines before the new entry is public.

**Answer:** _add reply here_

### Q: opendataloader-pdf has appeared in at least five consecutive builds with an 'investigate' recommendation; has any team member evaluated its extraction quality on a common test set relative to OCR-3, and should it be added to data/nanonets_context.md?

**Context:** Without a named entry in the competitive registry, each build evaluates opendataloader-pdf from scratch rather than tracking it as a known entrant alongside MinerU, Docling, and Unstructured. The same gap applies to BiSheng and RAGFlow. A single team response would stabilize scoring for all three across future builds.

**Answer:** _add reply here_

### Q: The arXiv and HN 403 failures have persisted for 11+ consecutive builds. Prior questions raised Semantic Scholar (build 2026-05-22T18:17:11) and OAI-PMH (build 2026-05-22T00:17:49) as alternatives, both unanswered. Should this be treated as a resolved policy decision — accept github_trending-only signal — or an unresolved infrastructure issue requiring a team decision by a specific date?

**Context:** Framing it as a policy decision would end the recurring infrastructure question. Without clarity, the build agent will surface the arXiv outage every build. If the team accepts github_trending-only signal as the operating norm, the context file should note this so future builds can adjust their editorial posture accordingly.

**Answer:** _add reply here_

---
