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

## Build 2026-05-23T12:00:00+00:00 (audit: partial)

### Q: Is HuggingFace Transformers the team's primary VLM training and fine-tuning framework, or does the team use a custom framework?

**Context:** ms-swift's GRPO support for InternVL3.5, Qwen3-VL, and GLM-5.1 is importable via transformers; if the team uses a custom framework, the competitive risk from ms-swift-powered external labs differs substantially from the tooling-ready scenario.

**Answer:** _add reply here_

### Q: Should the team proactively monitor HuggingFace for new LLaVA-OneVision-1.5 document-specific fine-tunes before they formally submit to the IDP Leaderboard?

**Context:** LLaVA-OneVision-1.5 training framework is trending; prior LLaVA-based fine-tunes have appeared on the IDP Leaderboard. Early awareness would allow preparation of benchmark baselines before a new entry is published.

**Answer:** _add reply here_

### Q: Does Nanonets Agentic Data Extraction have a first-party connector in Google's genkit or in any MCP-native framework such as UltraRAG?

**Context:** Both genkit (Google, production-grade) and UltraRAG (OpenBMB, MCP-native) are trending. Anthropic, OpenAI, and Google APIs already have genkit connectors; absence from these distribution channels means developers building on these frameworks default to other extraction services.

**Answer:** _add reply here_

### Q: Would a 1-2 day experiment comparing the knowledge-infused multimodal RAG approach's phantom-row reduction against the mechanistic interpretability baseline be feasible and publishable?

**Context:** A retrieval-based multimodal hallucination mitigation project has appeared in at least three consecutive builds. If retrieval-based mitigation achieves comparable phantom-row reduction at lower engineering cost, it could accelerate the production mitigation path while the interpretability work continues.

**Answer:** _add reply here_

---

## Build 2026-05-23T18:08:43+00:00 (audit: partial)

### Q: The all-open-source document AI stack (extraction + orchestration + evaluation + fine-tuning) is now fully represented in a single trending cycle. Has the team characterized the accuracy floor of an all-open-source pipeline relative to OCR-3 on a common benchmark (DocVQA, OmniDocBench, or the IDP Leaderboard test set)?

**Context:** lmms-eval, evalscope, Unstructured, opendataloader-pdf, Dify, RAGFlow, and ms-swift all trend this cycle. A concrete accuracy comparison — not just feature coverage — would allow the team to quantify the make-vs-buy gap and communicate it to customers. Without this, the competitive framing defaults to qualitative claims.

**Answer:** _add reply here_

### Q: Both lmms-eval and evalscope are trending without OCR-3 in their model registries. Should the team assign a specific person to submit OCR-3 to one or both framework registries, and is there a publication embargo or quality-gate concern with third-party benchmark access to early results?

**Context:** Competitors can already publish lmms-eval or evalscope comparisons against Qwen3-VL, GLM-5.1, and InternVL3.5 without including OCR-3. The absence is not a filter choice by these frameworks — it is a submission gap. Prior builds asked whether the team uses these frameworks internally; this question is specifically about external-facing registry inclusion.

**Answer:** _add reply here_

### Q: arXiv and HN have returned 403 errors for 13+ consecutive builds. Should this be treated as a resolved infrastructure policy — accept github_trending-only signal as the operating norm — or does the team intend to fix the access path by a specific date?

**Context:** Prior builds proposed Semantic Scholar (build 2026-05-22T18:17:11) and OAI-PMH (build 2026-05-22T00:17:49) as alternatives; neither has been acted on. Without arXiv, the vlm_research and doc_ai research_implication fields across all builds are inferred from GitHub repos rather than papers. Framing it as a resolved policy decision would end the recurring question; framing it as an open issue would clarify who owns the fix.

**Answer:** _add reply here_

### Q: SGLang provides RadixAttention and continuous batching for multimodal model serving. Has the team evaluated SGLang or an equivalent high-throughput serving framework for OCR-3, and is the current serving stack already comparable in throughput and per-token cost?

**Context:** OCR-3 is a 35B MoE model; serving at scale carries concrete per-token costs. Confirming whether the team already uses an equivalent framework would allow the dashboard to stop flagging SGLang as a new item each cycle. If not yet evaluated, a cost comparison against the current stack would determine whether migration is warranted.

**Answer:** _add reply here_

### Q: The orchestration-layer platforms (Dify, RAGFlow, UltraRAG) are trending without confirmed Nanonets Agentic Data Extraction connectors. Has the team established whether any of these platforms has a native or community-maintained Nanonets connector, and if not, is building one a prioritized distribution task?

**Context:** Without a native connector, developers adopting Dify, RAGFlow, or UltraRAG default to bundled open-source parsers (Unstructured, opendataloader-pdf). This is a distribution channel gap, not a product quality gap. A single community connector for the most-adopted platform would be actionable. Prior builds have asked about individual platforms; this consolidates the question.

**Answer:** _add reply here_

---

## Build 2026-05-24T12:00:00+00:00 (audit: partial)

### Q: Has a structured feature comparison between Unstructured.io's current release and the Nanonets Agentic Data Extraction /parse endpoint been conducted on a common test set?

**Context:** Unstructured.io has appeared in multiple consecutive builds and is the highest-scoring competitive item in this build (composite=58). Without a comparative benchmark, it receives 'monitor' indefinitely. A one-time feature matrix on common document types (invoices, contracts, tables) would allow future builds to score Unstructured releases against a fixed accuracy and feature baseline rather than re-evaluating from scratch.

**Answer:** _add reply here_

### Q: Has the team established an automated HuggingFace watch for new model cards referencing LLaVA-OneVision-1.5 plus document/OCR/IDP benchmarks?

**Context:** LLaVA-OneVision-1.5 training framework is trending this build; prior LLaVA-based fine-tunes have appeared on the IDP Leaderboard. Build 2026-05-23T12 asked whether the team proactively monitors these fine-tunes; that question is unanswered. This build surfaces a new framework version, raising the same concern at the next generation.

**Answer:** _add reply here_

### Q: RSS returned zero items this build for the first time — is the feed list stale, or was this a transient network failure?

**Context:** Prior builds relied on RSS as the sole working newsletter source alongside github_trending; arXiv and HN have been 403-ing for 15+ consecutive builds. If the RSS feeds have moved or discontinued, the current feed list in data/sources.yaml needs updating. Distinguishing stale URLs from a transient fetch timeout would determine whether editorial action is needed.

**Answer:** _add reply here_

### Q: Is there a defined customer segment where Firecrawl and the Nanonets /parse endpoint are directly substitutable, or do they address different document sources (web content vs. scanned/uploaded files)?

**Context:** Firecrawl is named in the editorial context as adjacent-competitive following Mendable's pivot, and this is its third or more consecutive trending appearance. Without a clear substitution boundary, the 'monitor' action persists without a threshold for escalation. A product-level definition of where the two overlap would sharpen future scoring and action recommendations.

**Answer:** _add reply here_

### Q: At what benchmark score on OlmOCR-Bench or DocVQA should a sub-7B document VLM be considered a material IDP Leaderboard entrant warranting escalated tracking?

**Context:** TinyLLaVA Factory enables small-parameter multimodal model training; the IDP Leaderboard currently lists large models. Without an explicit accuracy threshold, each small-model release receives 'monitor' indefinitely. A defined floor would allow future builds to automatically escalate or de-escalate small-model entries without per-build editorial judgment.

**Answer:** _add reply here_

---

## Build 2026-05-24T18:00:00+00:00 (audit: partial)

### Q: Should genkit-ai/genkit be treated as a priority distribution-connector target, distinct from community platforms like Dify and RAGFlow?

**Context:** Genkit is production-backed by Google with enterprise-grade SDKs in JS, Go, and Python; its connector set already includes Anthropic, OpenAI, and Gemini. Prior questions focused on Dify and RAGFlow; Genkit's Google backing and production-use trajectory make the absence of a Nanonets connector a qualitatively different distribution risk.

**Answer:** _add reply here_

### Q: Has the team established a benchmark baseline for cross-architecture hallucination transfer tests using smaller open VLMs?

**Context:** TinyLLaVA Factory and LLaVA-OneVision 1.5 both trend this cycle as accessible frameworks for training sub-7B document VLMs. Without a published baseline experiment using these model classes, the team cannot determine whether hallucination patterns from OCR-3 propagate to smaller open-weight models, which has direct implications for both research publication and IDP Leaderboard risk.

**Answer:** _add reply here_

### Q: Should SGLang be formally evaluated for OCR-3 serving cost rather than flagged each build?

**Context:** SGLang has appeared in five or more consecutive builds. The question is not whether it is relevant but whether the team has already made an informed decision to use or not use it. A single answer stating the current serving infrastructure and whether it was evaluated against SGLang would close this question permanently.

**Answer:** _add reply here_

### Q: Is the arXiv and HN 403 failure now a resolved policy — github_trending is the accepted source set — or is there an owner and deadline for restoring the other sources?

**Context:** arXiv and HN have returned 403 errors for 16+ consecutive builds; RSS returned zero items again this cycle. Without primary research sources, vlm_research and doc_ai framing fields are inferred from GitHub repository metadata alone. Prior builds proposed Semantic Scholar and OAI-PMH as alternatives; neither has been acted on. A clear policy decision would end the recurring infrastructure question.

**Answer:** _add reply here_

---

## Build 2026-05-24T12:16:50+00:00 (audit: partial)

### Q: Should the team monitor NVIDIA NeMo Automodel's GitHub forks for document-dataset fine-tunes that could produce IDP Leaderboard submissions?

**Context:** NeMo Automodel provides HuggingFace-compatible distributed VLM training backed by NVIDIA. ArXiv has been unavailable for 17+ consecutive builds, removing the primary early-warning channel for academic fine-tune submissions. A GitHub watch on NeMo forks that reference DocVQA, OmniDocBench, or IDP Leaderboard would partially substitute for the missing arXiv signal.

**Answer:** _add reply here_

### Q: UltraRAG and JeecgBoot both reference MCP-native integration in the same cycle. Is there an open-source or planned Nanonets MCP connector, and if not, is building one now prioritized?

**Context:** MCP is consolidating as an integration standard; this is the third consecutive cycle in which MCP-native platforms appear. Prior builds asked about MCP integration (builds 2026-05-23T12 and 2026-05-23T18); both are unanswered. The question is not about technical feasibility but about whether a connector is already in progress or queued.

**Answer:** _add reply here_

### Q: Does Ultralytics YOLO play any role in Nanonets document preprocessing, or does OCR-3 handle layout detection end-to-end?

**Context:** YOLO-family models are a common preprocessing step for document layout detection before VLM-based extraction. If OCR-3 handles layout natively at equivalent or better accuracy, this question can be permanently closed for future builds. If not, a YOLO preprocessing stage could improve table-cell accuracy on dense documents. A one-sentence answer would end recurring low-relevance scoring of YOLO items.

**Answer:** _add reply here_

### Q: The three most-recurring orchestration-layer competitors (Dify, BiSheng, UltraRAG) are all backed by Chinese AI organizations. Does this change the competitive threat profile relative to US-backed platforms like Genkit?

**Context:** Chinese-backed platforms may target different deployment patterns — on-premise enterprise, different regional markets — that partially de-overlap from Nanonets' typical customer base. If the threat is geographically segmented, future builds should reflect that in scoring and action recommendations rather than treating all orchestration platforms as interchangeable.

**Answer:** _add reply here_

### Q: The Gpt-Agreement-Payment repo (ChatGPT subscription protocol replay and hCaptcha bypass) appeared in github_trending this cycle with composite=0. Should such items be filtered at the ingest or scoring stage given potential reputational risk from including them in a public dashboard?

**Context:** The current github_trending keyword filter does not exclude tools designed for payment bypass or CAPTCHA circumvention. These items score zero and have no editorial relevance, but including them in state/run files that feed a public dashboard is a reputational consideration. A keyword exclusion list in sources.yaml would prevent recurrence.

**Answer:** _add reply here_

---

## Build 2026-05-24T18:14:23+00:00 (audit: partial)

### Q: Self-reflective hallucination-aware multimodal RAG has appeared in four or more consecutive builds; should 'read in week' be the standing default action for retrieval-based hallucination mitigation items, or does the team want to explicitly compare this paradigm against the mechanistic interpretability work on a shared benchmark?

**Context:** Without a confirmed stance on retrieval-based mitigation in the research scope, each build must independently decide whether to escalate or dismiss these items. A yes/no answer on whether the team actively tracks this paradigm would stabilize future action recommendations for the entire class of items.

**Answer:** _add reply here_

### Q: Three VLM training frameworks (NeMo Automodel, LLaVA-OneVision-1.5, TinyLLaVA_Factory) trended in a single build cycle; should the build automatically flag GitHub repos that combine any of these frameworks with DocVQA, OmniDocBench, or IDP Leaderboard references as potential upcoming leaderboard submissions requiring escalated tracking?

**Context:** Manual per-item evaluation cannot anticipate submissions; an automated watch rule would provide advance notice before a fine-tune is publicly submitted. The rule would not require editorial judgment from the build agent, only keyword matching at the ingest stage.

**Answer:** _add reply here_

### Q: Genkit (Google-backed) and the Chinese-backed orchestration tier (Dify, BiSheng, JeecgBoot, UltraRAG) both trend this cycle without confirmed Nanonets connectors; should the editorial grounding differentiate these tiers by geographic deployment profile so future builds can score and prioritize connector gaps accurately?

**Context:** Chinese-backed platforms may target on-premise enterprise deployments in different regional markets than Nanonets' typical customer base. Treating both tiers as a single orchestration category may over- or under-estimate the connector gap depending on the team's go-to-market focus. Prior builds asked about individual platforms; this question is about the taxonomic grouping.

**Answer:** _add reply here_

### Q: The Gpt-Agreement-Payment item (ChatGPT subscription protocol replay with hCaptcha solver) has appeared in github_trending for two consecutive builds and scores composite=0. Should sources.yaml add a keyword exclusion list — e.g., 'captcha', 'bypass', 'subscription replay', 'anti-fraud' — to filter payment-circumvention tools at ingest before they appear in state/run files consumed by a public dashboard?

**Context:** These items carry reputational risk if the public dashboard ever links to or surfaces them. The current keyword filter in sources.yaml does not exclude them. A short exclusion list would prevent recurrence without requiring editorial judgment from the build agent.

**Answer:** _add reply here_

### Q: This is the nineteenth or more consecutive build with no arXiv or HN coverage; the two prior proposed alternatives (Semantic Scholar API and arXiv OAI-PMH) remain unanswered. Should the team treat github_trending-only signal as the accepted operating norm and note this in data/nanonets_context.md, or assign an owner and deadline for restoring a primary-research source?

**Context:** Without a policy decision, the build will continue surfacing this as an open infrastructure question every cycle. If github_trending-only is the accepted norm, a note in context.md would allow the build agent to adjust editorial posture — specifically, to set lower confidence priors on vlm_research and doc_ai research_implication fields that currently lack paper-based grounding.

**Answer:** _add reply here_

---

## Build 2026-05-25T00:15:46+00:00 (audit: partial)

### Q: Does OCR-3's five-endpoint architecture (/parse, /extract, /split, /chunk, /vqa) map to the omni-modality serving pattern that vllm-omni is optimized for, or is the endpoint structure better served by standard vLLM with separate decode configurations?

**Context:** vllm-omni appeared this cycle as the first item to split from vLLM specifically for omni-modality models. A one-sentence answer about the internal serving architecture would allow future builds to score vllm-omni as directly relevant infrastructure rather than re-evaluating it alongside standard vLLM each cycle.

**Answer:** _add reply here_

### Q: Should retrieval-based VLM hallucination mitigation (self-reflective-rag, knowledge-infused-multimodal-retrieval) receive a standing action recommendation that persists across builds, or does the team want to evaluate each new retrieval-mitigation item independently?

**Context:** Both items address phantom-row and structural hallucination classes via retrieval augmentation rather than mechanistic interpretability. They have appeared in at least four consecutive builds; without a confirmed team stance on whether this paradigm is inside or outside the research scope, each build must make an independent action recommendation for the same class of work.

**Answer:** _add reply here_

### Q: Could a prefilled-extraction-schema approach analogous to Zero-shot-PGT's prefilled-response image detection technique serve as a self-consistency check for phantom-row detection in OCR-3 outputs — specifically, does the model's extraction agree with itself when the target schema is injected at different context positions?

**Context:** Zero-shot-PGT demonstrated that prefilled token sequences improve zero-shot detection of AI-generated content in images. The equivalent question for document extraction is whether prefilling an extraction schema at different positions in the prompt changes which table rows the model hallucinates — if so, the disagreement signal is a cheap phantom-row detector that does not require mechanistic interpretability tooling.

**Answer:** _add reply here_

### Q: With vLLM, SGLang, and vllm-omni all trending simultaneously, should the build adopt a reference serving framework assumption for OCR-3 to avoid re-evaluating all three each cycle?

**Context:** All three frameworks are individually relevant to OCR-3 serving and appear in the same build cycle. If the team has already evaluated or selected one, naming it would allow future builds to score the others as 'monitor' rather than 'read in week' and would end a recurring multi-item review for the same infrastructure decision.

**Answer:** _add reply here_

---

## Build 2026-05-25T06:05:25.431991+00:00 (audit: partial)

### Q: arxiv, HN, and RSS all failed in this build (403 for arxiv and HN; no items for RSS). Is this a network policy issue in the remote execution environment, or do these endpoints require authentication not yet configured?

**Context:** Three of four sources have now failed in multiple consecutive builds. Without primary-research sources, the dashboard is structurally limited to GitHub Trending and cannot surface academic papers, community discussions, or frontier-lab blog posts. The pattern is consistent enough to suggest an environment-level issue rather than a transient error.

**Answer:** _add reply here_

### Q: opendataloader-pdf appeared in at least two prior builds and scored competitive=3 again here. Should it be added to the competitive registry in data/nanonets_context.md?

**Context:** This question was raised in the 2026-05-21T12:08 build and remains unanswered. Persistent GitHub Trending presence suggests non-trivial developer traction. A confirmed answer would change how future builds score and frame it.

**Answer:** _add reply here_

### Q: GLM-5 now appears in Ollama's supported model description; GLM-OCR is in the competitive set but GLM-5 is not. Is GLM-5 a distinct model from GLM-OCR, or the same product family?

**Context:** This question was raised in the 2026-05-21T12:08 build and remains unanswered. If GLM-5 includes document-extraction capabilities comparable to GLM-OCR, it should be added to the competitive registry. If not, items referencing GLM-5 may be over-scored on the competitive axis.

**Answer:** _add reply here_

### Q: Since all three primary-research sources (arxiv, HN, RSS) are failing across multiple builds, should trend analysis and the framing pass be explicitly flagged as 'infrastructure-biased' when fewer than 2 primary research sources contributed?

**Context:** The current signal derives entirely from GitHub Trending. Trends inferred from this mix reflect production tooling activity, not the research frontier. The framing pass lacks arxiv-based hallucination and VLM internals coverage that grounds the research_implication field.

**Answer:** _add reply here_

---

## Build 2026-05-25T12:00:00+00:00 (audit: partial)

### Q: arXiv, HN, and RSS have failed for 20+ consecutive builds; should github_trending-only signal be treated as the accepted operating norm, or is there an owner and deadline for restoring a primary-research source?

**Context:** Prior builds proposed Semantic Scholar (build 2026-05-22T18:17) and arXiv OAI-PMH (build 2026-05-22T00:17) as alternatives; neither has been acted on. Without arXiv, the vlm_research and doc_ai research_implication fields are inferred from GitHub repository metadata alone, which changes the epistemic status of all framing. A one-sentence policy decision would end the recurring infrastructure question.

**Answer:** _add reply here_

### Q: Should OCR-3 be submitted to the lmms-eval and/or evalscope model registries before a competitor uses either framework to publish a head-to-head comparison that structurally excludes OCR-3?

**Context:** Both frameworks are trending this cycle with Qwen3-VL, GLM-5.1, and InternVL3.5 registered. Build 2026-05-23T18 first raised OCR-3 registry submission as a distinct publishing decision. This question is specifically about external-facing benchmark visibility — not internal usage. A response stating whether there is an embargo, quality-gate, or assigned owner would close this question permanently.

**Answer:** _add reply here_

### Q: At what OmniDocBench or DocVQA score should a GRPO-fine-tuned open-weight model (Qwen3-VL, InternVL3.5) be classified as a material IDP Leaderboard threat warranting escalated tracking?

**Context:** ms-swift now provides an accessible GRPO pipeline for these model families; the toolchain lowers the submission barrier substantially. Build 2026-05-23T06 asked this question; it remains unanswered. A defined accuracy threshold would allow future builds to automatically escalate or dismiss GRPO-fine-tuned submissions without per-build editorial judgment.

**Answer:** _add reply here_

### Q: Should MinerU be added to the named competitive set in data/nanonets_context.md alongside Reducto, LlamaParse, and Docling?

**Context:** MinerU (opendatalab/Shanghai AI Lab) has appeared at the top of the competitive axis across more than ten consecutive builds and targets the identical PDF-to-LLM-ready markdown/JSON interface as Nanonets Agentic Data Extraction. Build 2026-05-21T18 first raised this question; it has not been answered. A one-word yes/no decision would allow stable scoring across future builds rather than per-build re-evaluation.

**Answer:** _add reply here_

### Q: Should retrieval-based VLM hallucination mitigation (self-reflective-rag, Knowledge-Infused Multimodal Retrieval) receive a standing action recommendation across builds, or does the team want each new retrieval-mitigation item evaluated independently?

**Context:** Both paradigms address phantom-row and structural hallucination classes via retrieval rather than mechanistic interpretability; they have appeared in at least five consecutive builds. Builds 2026-05-23T06 and 2026-05-25T00 both raised this question without a team response. A yes/no on whether retrieval-based mitigation is inside the research scope would stabilize action recommendations for the entire item class.

**Answer:** _add reply here_

---
