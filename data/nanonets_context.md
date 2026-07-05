# Nanonets Context — editorial grounding for the Landscape Monitor

This file is the system prompt that grounds every relevance-scoring and
framing decision made by the build agent. It is **public** (this repo is
public), so it contains no internal strategy, no per-stakeholder priorities,
no roadmap. Anything internal-only belongs in a team-private surface, not
here.

To retune what the dashboard surfaces, edit this file. The next build will
use the new context.

---

## What Nanonets is

Nanonets is a document-AI company. The core product is structured
information extraction from unstructured documents — invoices, receipts,
forms, contracts, tables, charts, IDs. The current public positioning is
two-pronged:

- **Nanonets Agents** — end-to-end process-automation agents that read
  messy inputs, apply customer-defined rules, and complete work inside
  systems of record (ERPs, inboxes, approval chains). Marketed for
  Accounts Payable, Order Management, Logistics, Healthcare RCM,
  Contracts, Vendor Onboarding, ID & Insurance.
- **Nanonets Agentic Data Extraction** — a document-extraction API
  surface built for LLM and agent pipelines: markdown + JSON output,
  table preservation, no-template setup, LangChain / LlamaIndex
  integrations.

The current flagship public model is **`Nanonets OCR-3`** — a
~35B-parameter Mixture-of-Experts VLM released April 2, 2026, ranked #1
on the IDP Leaderboard (85.9), OLM-OCR (87.4), and OmniDocBench (90.5)
as of launch. It exposes five canonical endpoints (`/parse`, `/extract`, `/split`,
`/chunk`, `/vqa`) and is positioned as "the only OCR model you need for
your entire agentic stack." Items that name OCR-3 directly, evaluate it,
or compare against it are **highest-priority relevant**.

Earlier still-public model artifacts the team maintains on Hugging Face:

- `nanonets/Nanonets-OCR2-3B` (Oct 2025, ~4B params) — prior generation,
  widely downloaded, still a common comparison baseline.
- `nanonets/Nanonets-OCR2-1.5B-exp` (Dec 2025, ~2B params) — small
  experimental variant.
- `nanonets/Nanonets-OCR-s` (Jun 2025) — earliest public OCR model.

Items that name or build on any of these models are relevant; OCR-3
takes precedence as the headline artifact.

The team also publicly maintains the **IDP Leaderboard**
(`idp-leaderboard.org` / `benchmarking.nanonets.com`), an academic
benchmark on document AI co-developed with IIT Indore. Items that
publish leaderboard results, contest its methodology, or are released by
models near the top of it (GPT-5.4, GPT-5.5, Gemini-3-Pro/Flash,
Gemini 3.1 Pro, Gemini 3.5 Flash, Claude 4.6 family, Claude Fable 5,
Claude Opus 4.8, Qwen3-VL, Pixtral, GLM-OCR, Chandra OCR 2,
LightOn OCR-2, DeepSeek-OCR 2) are competitive-axis relevant.

## Active research direction

The applied-AI-research team's primary public research line is
**hallucinations in vision-language models, broadly**. This includes
several subtypes that all matter:

- **Phantom-row hallucinations** — VLM tables that include rows the source
  document doesn't contain.
- **Repetition loops** — the model gets stuck reproducing the same
  fragment.
- **Infinite generation** — the model fails to emit EOS and keeps
  generating until the token budget runs out.
- **Structural hallucinations** — fake markers, mis-rendered captions,
  fabricated headers, mis-attributed fields.
- **Cross-architecture hallucination transfer** — does a hallucination
  pattern observed in one VLM family appear in another?

Methodology spans mechanistic interpretability (logit lens, activation
patching, causal scrubbing, sparse autoencoders, steering vectors, tuned
lens) and behavioral evaluation. Items about VLM internals, hallucination
characterization, or runtime mitigation are research-axis relevant.

## Competitive set (Document AI)

Items that name, compare against, or are released by these companies are
**competitive-axis relevant**:

- **Mistral OCR 4 / Mistral Document AI** — direct competitor on
  multilingual document extraction; Mistral OCR 4 (released June 23,
  2026; model ID mistral-ocr-4-0; mistral-ocr-latest alias now points
  to this version) adds bounding boxes, typed-block labels (titles,
  tables, equations, signatures), per-word confidence scores, and
  self-hosted single-container deployment; supports 170 languages
  across 10 language groups; priced at $4 per 1,000 pages ($2 with
  Batch API 50% discount); 85.20 on OlmOCRBench; 72% average win rate
  over tested systems in independent annotation. Supersedes Mistral OCR
  3 (January 2026; mistral-ocr-2512; 74% win rate over OCR 2). Mistral
  OCR 25.03 on Azure AI Foundry; Mistral OCR 25.05 on Vertex AI (May
  2026). Mistral OCR 2 retired June 30, 2026.
- **Reducto** — competitor on structured extraction with multi-pass
  agentic correction; exposes Parse / Extract / Split / Edit endpoints
  similar to OCR-3's surface. Raised $75M Series B (Andreessen
  Horowitz, February 2026); launched Deep Extract agentic product;
  released Classification endpoint (May 2026) for lightweight document
  categorization before downstream processing; Smart Schema in Studio
  (April 2026) for autonomous schema creation; 1 billion pages processed
  to date; acquired Opennote (May 2026), an AI-notebook startup, to
  strengthen agentic document-retrieval workflows; Reducto Deep Extract
  ranked #1 on LongExtractBench (announced July 1, 2026; independently
  audited by micro1; 225 sourced documents averaging 88,700+ fields
  each; 100% completeness, 99.6% precision, 99.6% recall, 99.3% leaf
  accuracy; zero failures; peer systems: Extend MAX, LlamaExtract-Agentic,
  GPT-5.5, Claude Opus 4.8, Gemini 3.1 Pro).
- **LlamaParse (LlamaIndex / LlamaCloud)** — managed parsing service
  inside LlamaCloud; RAG-native, multimodal, often paired with or
  benchmarked against Reducto. LlamaParse v2 launched 2026 with
  simplified tier config and ~50% cost reduction. LlamaIndex also
  open-sourced LiteParse, a lightweight TypeScript-native local parser
  (March 2026). ParseBench launched April 2026 as a LlamaIndex-run
  document-OCR benchmark for AI agents; ParseBench accepted to CVPR
  2026. LlamaParse Agentic Plus mode adds bounding-box citations for
  complex formulas, handwriting, and infographics; word-, line-, and
  cell-level bounding boxes added for audit-grade citation trails.
  Parse-Flow launched June 2026 for visual document intelligence
  workflows.
- **Unstructured.io** — competitor and frequent integration partner;
  document parsing infrastructure. Expanded Microsoft Azure integration
  announced June 3, 2026, covering Azure AI Search and Blob Storage
  pipelines for enterprise RAG and agentic workflows.
- **Extend** (extend.ai; YC-backed; raised $17M) — end-to-end document
  processing competitor positioning as "the document processing cloud";
  unifies models, infrastructure, and tooling into a single platform for
  production document-to-structured-data pipelines; appeared as a direct
  peer system in LongExtractBench (July 2026) alongside Reducto, Llama-
  Extract-Agentic, GPT-5.5, Opus 4.8, and Gemini 3.1 Pro.
- **Docling** (IBM Research) — open-source layout-aware document parser;
  reference architecture and common open-source baseline.
  Granite-Docling-258M (production VLM, January 2026, Apache 2.0)
  replaced SmolDocling; project donated to Linux Foundation Agentic AI
  Foundation alongside BeeAI. IBM released the Heron layout model (IBM
  Think 2026; 23.5% mAP improvement over prior Docling baseline; Heron-101
  variant processes pages at 28ms on A100). Docling for IBM watsonx
  reached general availability (June 2026; $4/1,000 pages flat, 20% below
  comparable major vendors per IBM list pricing).
- **Chandra OCR 2 / LightOn OCR-2** — specialized OCR-VLM models that
  OCR-3 benchmarks against; Chandra OCR 2 (Datalab, March 2026) is a
  4B-parameter model built on Qwen 3.5, 85.9% on olmOCR benchmark,
  supporting 90+ languages. LightOn OCR-2 is a 1B end-to-end VLM
  optimized for OlmOCR-Bench.
- **GLM-OCR** (Zhipu AI, March 2026; 0.9B params, 94.62 on OmniDocBench
  V1.5), **DeepSeek-OCR 2** (DeepSeek AI, January 2026; 3B params, 91.09%
  on OmniDocBench v1.5), **HunyuanOCR** (Tencent Hunyuan, November 2025;
  1B params; 94.1 on OmniDocBench; end-to-end OCR-VLM covering detection,
  recognition, parsing, and extraction; 100+ languages; MIT license),
  **Qianfan-OCR** (Baidu Qianfan, March 2026; 4B params; 93.12 on
  OmniDocBench v1.5, 880 on OCRBench; unified end-to-end document
  intelligence VLM with "Layout-as-Thought" architecture; open-weight on
  Hugging Face), **PaddleOCR-VL-1.6** (PaddlePaddle/Baidu, released May
  28, 2026; ~0.9B VLM + PP-DocLayoutV3 layout model; 96.33 on OmniDocBench
  v1.6, #1 on that benchmark version; open-weight),
  **Unlimited-OCR** (Baidu, released June 22, 2026; 3B MoE with 500M
  activated parameters; R-SWA architecture keeps KV cache constant for
  long-document single-pass parsing; 93.23 on OmniDocBench v1.5, 93.92
  on v1.6; 20–40+ page documents handled in a single pass; MIT license;
  arXiv 2606.23050; GitHub baidu/Unlimited-OCR),
  **Surya OCR 2** (Datalab, released May 27, 2026; 650M params; same
  team as Chandra OCR 2; 83.3% on OlmOCR-bench; 91 languages, 87.2%
  multilingual pass rate; Apache 2.0 code / modified OpenRAIL-M weights),
  **Pixtral** (Mistral),
  **Qwen3-VL** family (Alibaba; Qwen 3.6-VL is the 2026-series variant),
  **Llama-3.2-Vision** (Meta) — open-weight VLMs that appear on the IDP
  Leaderboard as direct comparables. Note: OmniDocBench was updated from
  v1.5 to v1.6 (April 10, 2026; +296 pages, MGAM evaluation methodology)
  and then v1.7 (April 30, 2026); scores across versions are not directly
  comparable.
- **Rossum** (acquired by Coupa, announced Inspire 2026), **Docsumo**,
  **ABBYY**, **Kofax (Tungsten Automation)** — legacy / semi-structured
  document-extraction vendors Nanonets routinely positions against
  publicly.
- **Firecrawl** (Mendable team) — adjacent: web-to-markdown extraction,
  not document AI proper, but increasingly cited as a data-prep
  alternative for agent pipelines. PDF Parser v2 (February 2026), the
  Fire-PDF Rust engine (April 2026), and a dedicated /parse endpoint
  (May 2026; supports PDFs, Word docs, spreadsheets up to 50MB; 5×
  faster than prior engine) continue moving Firecrawl closer to
  document AI proper. Note that **Mendable as a standalone product is
  effectively deprecated** — the same team has pivoted to Firecrawl.
- **Tesseract** — legacy OCR baseline; releases of OCR-VLM models that
  benchmark against Tesseract are worth surfacing.
- **Frontier-lab vision-for-docs offerings** — see the rule below.

## Frontier-lab signal

Items from Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral, xAI, and
Hugging Face touch this dashboard in two distinct ways. **Disambiguate
strictly**:

### Rule (axis disambiguation, strict)

When a frontier lab releases a vision / document / multimodal capability
that **directly overlaps Nanonets' product surface** — extraction,
parsing, layout-aware OCR, document VQA, table extraction, schema-based
extraction, batch document processing — the item's `primary_axis`
**MUST** be `competitive`. Set `frontier` as a `secondary_axis`. The
frontier lab is, on that specific item, a competitor.

Examples that are **competitive-primary**:

- Anthropic ships a document-extraction tool inside Claude / the API;
  Claude Fable 5 (June 9, 2026; model ID claude-fable-5) and Claude
  Mythos 5 (limited availability, Project Glasswing) include advanced
  vision understanding for diagrams and nested tables and appear on
  ParseBench; Claude Opus 4.7 (April 16, 2026) accepts images up to
  2,576px on the long edge (~3.75 megapixels, 3x prior models) with
  improved chart and document parsing accuracy; Claude Opus 4.8 (May 28,
  2026) adds dynamic multi-agent workflows and is evaluated as a peer on
  long-document structured extraction benchmarks (LongExtractBench,
  July 2026).
- Google releases a Gemini-document-mode endpoint or a layout-aware
  OCR benchmark result (Gemini 3 Pro/Flash; Gemini 3.1 Pro released
  February 19, 2026; Gemini 3.5 Flash released May 2026 at Google I/O).
- OpenAI announces GPT-5.x vision improvements on DocVQA / ChartQA /
  OmniDocBench / IDP Leaderboard (GPT-5.4 March 2026, GPT-5.5 April
  2026).
- Mistral OCR is updated with new accuracy or pricing (Mistral OCR 4
  released June 23, 2026).
- xAI ships Grok vision document handling; the Grok Collections API
  (released 2026) uses OCR and layout-aware parsing to extract and
  index PDFs and Excel files into searchable knowledge bases for RAG
  workflows ($2.50/1,000 searches).
- Meta releases a Llama-vision model with explicit document focus.

The `frontier` axis is reserved for capability releases that **do not
directly compete** on the extraction product surface. Examples that are
**frontier-primary**:

- A new reasoning model with no document focus (e.g., a math /
  code-reasoning release).
- A new agent platform / orchestration framework with no document
  parser.
- A context-length improvement that doesn't include document-AI
  benchmarks.
- An infrastructure release (e.g., a new training framework, a new
  serving library, a new safety eval suite).
- A pure-text capability (e.g., long-form writing, multilingual chat).

Tie-break: if you're unsure whether an item competes with the OCR-3 /
Agentic Data Extraction surface, default to `competitive`. The cost of
under-counting a competitor is higher than the cost of over-counting
one.

### Frontier-lab signal (general)

Beyond the disambiguation rule, items from these labs are
frontier-axis relevant when they touch:

- Capability releases (new model launches, modality upgrades) that
  don't directly compete.
- Evaluation results that move the SOTA on relevant benchmarks (DocVQA,
  ChartQA, InfoVQA, FUNSD, CORD, OmniDocBench, OlmOCR-Bench, IDP
  Leaderboard, ICDAR competitions).
- Pricing / accessibility changes that shift the make-vs-buy calculus
  for document-AI startups.
- Agent-platform moves that affect document-AI workflows.

## What's explicitly NOT in this context

- Internal paper-submission targets, venue commitments, or deadlines.
- Per-stakeholder strategic priorities (e.g., what Prathamesh
  personally cares about).
- Internal product roadmap or customer-specific information.
- Hiring plans, financial details, or partnership negotiations.
- Names or details of Nanonets customers.

If the dashboard's framing ever references any of the above, it has
leaked content that doesn't belong in a public artifact. Remove it.

## Editorial voice

Analyst-grade, terse, no hype, no emoji, no marketing copy. Reference
points:

- **Stratechery** for framing.
- **The Information** for sourcing posture.
- **Interconnects** for technical voice.

Avoid:

- "Exciting." "Game-changing." "Revolutionary." "Stunning." "Amazing."
- Rocket / fire / any emoji.
- Cliffhangers, breathless reveals, click-bait.
- Speculation framed as fact.

## When in doubt

If an item could plausibly appear in two axes, set `primary_axis` to the
more specific of the two (Document AI > Competitive > Frontier > VLM
research as the tie-breaking order). List the rest in `secondary_axes`.
The frontier-vs-competitive disambiguation rule above is **strict** and
overrides this general tie-breaker when a frontier lab ships an
extraction-surface capability.

If an item names Nanonets directly in a critical or negative context,
set `hostility_flag: true`. The framing template for such items is
**descriptive, not defensive** — describe how the source positions
Nanonets, do not respond.

## Last updated

**Date:** 2026-05-21

**Sources consulted:**

- `nanonets.com` — current product positioning (Nanonets Agents,
  Nanonets Agentic Data Extraction, OCR-3 as flagship)
- `nanonets.com/blog` — recent post titles through April 2026
- `nanonets.com/research/nanonets-ocr-3` (via search snippet) — OCR-3
  release details (April 2, 2026; 35B MoE; #1 IDP Leaderboard)
- `huggingface.co/nanonets` — current public model lineup (OCR-s,
  OCR2-3B, OCR2-1.5B-exp)
- `benchmarking.nanonets.com/models` — current IDP Leaderboard
  competitive set (GPT-5.4, Gemini-3-Pro/Flash, Claude 4.6 family,
  Qwen, Pixtral, GLM-OCR, Llama-3.2-Vision)
- `llamaindex.ai`, `reducto.ai`, `firecrawl.dev` — competitive
  positioning of LlamaParse, Reducto, Firecrawl
- arXiv search — no Nanonets-authored 2026 papers surfaced publicly;
  research direction phrasing left unchanged

**Material changes versus prior version:**

- Replaced flagship-model section: OCR-3 is now the headline; OCR2-3B
  demoted to "prior generation."
- Added current product surfaces (Nanonets Agents; Agentic Data
  Extraction API with `/parse`, `/extract`, `/split`, `/chunk`,
  `/vqa`).
- Expanded competitive set: added LlamaParse, Chandra OCR, LightOn
  OCR-2, GLM-OCR, Pixtral, Qwen-VL, Llama-3.2-Vision, Rossum,
  Docsumo, ABBYY, Kofax, Firecrawl.
- Flagged Mendable as effectively deprecated (team pivoted to
  Firecrawl).
- Added IDP Leaderboard as a Nanonets-maintained competitive surface.
- Rewrote the frontier-lab section with a strict
  axis-disambiguation rule per the task brief: frontier-lab vision /
  document releases that overlap Nanonets' product surface MUST be
  scored `primary_axis: competitive`.
- Added OmniDocBench and OlmOCR-Bench to the benchmark list.
- Research-direction section unchanged; no public Nanonets-authored
  2026 papers surfaced to justify a rewrite.

---

**Date:** 2026-05-24

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com` —
  all returned HTTP 403; fell back to web search for all Nanonets data
- WebSearch: "Nanonets OCR-3 2026" — confirmed #1 on IDP Leaderboard
  at 85.9% overall; release date April 2, 2026 verified
- WebSearch: "site:huggingface.co/nanonets" — model lineup unchanged
  (OCR-s, OCR2-3B, OCR2-1.5B-exp)
- WebSearch: "nanonets arxiv 2026" — no team-authored papers surfaced
- WebSearch: IDP Leaderboard 2026 rankings
- WebSearch: Mistral OCR 2026 — Mistral OCR 3 (January 2026),
  Mistral OCR 25.03 (May 2026)
- WebSearch: Reducto AI 2026 — $75M Series B, Deep Extract, Opennote
  acquisition
- WebSearch: LlamaParse / LlamaIndex 2026 — v2, LiteParse
- WebSearch: Chandra OCR / LightOn OCR 2026 — Chandra OCR 2 (Datalab,
  March 2026)
- WebSearch: GLM-OCR Zhipu AI 2026 — March 2026 release confirmed
- WebSearch: DeepSeek OCR vision 2026 — DeepSeek-OCR 2 (January 2026)
- WebSearch: Docling IBM 2026 — Granite-Docling-258M, Linux Foundation
- WebSearch: Qwen-VL 2026 — Qwen3-VL / Qwen 3.6-VL confirmed
- WebSearch: Rossum Docsumo ABBYY Kofax 2026 — Coupa/Rossum
  acquisition; Kofax rebranded Tungsten Automation
- WebSearch: Firecrawl 2026 — PDF Parser v2, Fire-PDF Rust engine
- WebSearch: OpenAI GPT-5.5 document vision 2026 — April 23, 2026
- WebSearch: Google Gemini document OCR 2026 — Gemini 3.5 Flash at
  Google I/O, May 19, 2026
- WebSearch: xAI Grok vision document 2026 — vision capabilities
  present but no dedicated document extraction product

**Material changes versus prior version (2026-05-21):**

- Added DeepSeek-OCR 2 (DeepSeek AI, January 2026; 3B params; 91.09%
  on OmniDocBench v1.5) as a new entrant in the competitive set.
- Updated Mistral OCR to reflect Mistral OCR 3 (January 2026) and
  Mistral OCR 25.03 (May 2026) as current versions.
- Reducto: noted $75M Series B (a16z, February 2026) and Deep Extract
  product; 1 billion pages processed milestone.
- Rossum acquired by Coupa (announced Inspire 2026); Kofax rebranded
  as Tungsten Automation. Both retained in competitive set with notes.
- Updated LlamaParse to reflect v2 launch and LiteParse open-source
  release (March 2026).
- Updated Chandra OCR to v2 (Datalab, March 2026; Qwen 3.5 base).
- Updated Docling to reflect Granite-Docling-258M (January 2026) and
  Linux Foundation Agentic AI Foundation donation.
- Updated Qwen-VL references to Qwen3-VL / Qwen 3.6-VL (2026 series).
- Added GPT-5.5 (April 2026) and Gemini 3.5 Flash (May 2026) to IDP
  Leaderboard comparables list and frontier-lab examples.
- Added Firecrawl PDF Parser v2 and Fire-PDF engine note (February
  2026); classification as "adjacent" unchanged.
- GLM-OCR March 2026 release and OmniDocBench V1.5 score (94.62)
  confirmed and added inline.
- No changes to research-direction section; no new Nanonets-authored
  arXiv papers found.
- Nanonets OCR-3 #1 ranking on IDP Leaderboard confirmed unchanged.

---

**Date:** 2026-05-31

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 2026 IDP leaderboard" — #1 at 85.9%
  confirmed unchanged; April 2026 release date confirmed
- WebSearch: "huggingface nanonets OCR-3 2026" — OCR-3 confirmed
  API-only (not open-weight on Hugging Face); prior open-weight lineup
  (OCR-s, OCR2-3B, OCR2-1.5B-exp) unchanged
- WebSearch: "nanonets arxiv 2026" — no team-authored papers surfaced
- WebSearch: Mistral OCR 2026 — OCR 3 (January 2026 announcement;
  model ID mistral-ocr-2512 = December 2025) confirmed; 25.03 on
  Azure AI Foundry, 25.05 on Vertex AI; versioning label in prior
  context ("25.03 is May 2026 update") could not be independently
  confirmed; text left unchanged pending manual verification
- WebSearch: Reducto AI 2026 — Series B and Deep Extract confirmed;
  Opennote acquisition (May 7, 2026) confirmed from reducto.ai blog
  and multiple trade sources
- WebSearch: LlamaParse / LlamaIndex 2026 — v2 and LiteParse
  confirmed; ParseBench (LlamaIndex-run document-OCR benchmark for
  AI agents) launched; LlamaSheets and LlamaSplit noted as adjacent
  new products
- WebSearch: Chandra OCR / LightOn OCR 2026 — Chandra OCR 2 (Datalab,
  March 2026) and LightOnOCR-2 (January 2026) confirmed
- WebSearch: GLM-OCR Zhipu AI 2026 — March 2026 release and 94.62
  OmniDocBench score confirmed
- WebSearch: DeepSeek OCR 2026 — January 2026 release and specs
  confirmed
- WebSearch: "Tencent Hunyuan OCR 2026" — HunyuanOCR (November 2025;
  1B params; 94.1 on OmniDocBench; 100+ languages; MIT license)
  confirmed as new entrant not previously listed; covered alongside
  GLM-OCR and DeepSeek-OCR in open-model OCR benchmarks
- WebSearch: Docling IBM 2026 — Granite-Docling-258M and Apache 2.0
  license confirmed
- WebSearch: Qwen3-VL 2026 — Qwen3-VL family confirmed; Qwen3-VL-Plus
  named as flagship API variant; Qwen 3.6-VL reference unchanged
- WebSearch: Rossum/Docsumo/ABBYY/Kofax 2026 — all confirmed
  operating; Coupa/Rossum acquisition and Kofax/Tungsten Automation
  rebrand previously noted, still current
- WebSearch: Firecrawl 2026 — Fire-PDF Rust engine and PDF Parser v2
  confirmed; pdf-inspector open-source library noted
- WebSearch: Anthropic Claude document extraction 2026 — no dedicated
  document-extraction product announced; vision capabilities via
  standard API unchanged
- WebSearch: OpenAI GPT-5 document vision 2026 — GPT-5.4 confirmed
  active for document understanding; no dedicated extraction product
- WebSearch: Google Gemini 3.5 Flash 2026 — confirmed launched at
  Google I/O May 20, 2026; used in OCR-backed document workflows by
  enterprise customers; already reflected in prior context

**Material changes versus prior version (2026-05-24):**

- Added HunyuanOCR (Tencent Hunyuan, November 2025; 1B params; 94.1
  on OmniDocBench) to the competitive set as a new entrant not
  previously listed; confirmed coverage alongside GLM-OCR and
  DeepSeek-OCR 2 in open-model OCR benchmark comparisons.
- Updated Reducto entry: added Opennote acquisition (May 7, 2026), an
  AI-notebook startup acquired to strengthen agentic document-retrieval
  workflows.
- No material changes to Nanonets OCR-3 positioning, IDP Leaderboard
  ranking, or research-direction section.
- All other competitive entries confirmed still operating; no companies
  renamed, acquired beyond prior notes, or pivoted since last refresh.
- Note for manual verification: the label "Mistral OCR 25.03 is the
  May 2026 update" in the Mistral entry could not be confirmed from
  public sources; 25.03 appears on Azure AI Foundry as an earlier
  checkpoint (naming convention YY.VV or YY.MM), not a May 2026
  release. Team should verify and correct if needed.

---

**Date:** 2026-06-07

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 IDP leaderboard 2026 ranking" — #1 at
  85.9% confirmed; official Nanonets X post (@nanonets) provides
  additional scores: 87.4 on OLM-OCR (Global #1), 90.5 on OmniDocBench
- WebSearch: "Nanonets product announcement blog June 2026" — no June
  2026 announcements indexed; most recent posts from March 2026
- WebSearch: "site:huggingface.co/nanonets" — open-weight model lineup
  unchanged (OCR-s, OCR2-3B, OCR2-1.5B-exp); OCR-3 remains API-only
- WebSearch: "nanonets arxiv 2026" — no team-authored papers surfaced
- WebSearch: Mistral OCR 2026 — Mistral OCR 25.05 confirmed on Vertex AI
  (Google Cloud docs last updated May 8, 2026; model ID mistral-ocr-2505);
  Mistral OCR 25.03 confirmed on Azure AI Foundry; prior label "25.03
  is the May 2026 update" corrected
- WebSearch: Reducto AI 2026 — Classification endpoint (May 21, 2026)
  and Smart Schema in Studio (April 2026) confirmed from reducto.ai blog
- WebSearch: LlamaParse / LlamaIndex 2026 — ParseBench (April 2026)
  and LlamaParse Agentic Plus visual grounding confirmed from
  llamaindex.ai newsletters
- WebSearch: Docling IBM 2026 — Heron layout model (IBM Think 2026;
  23.5% mAP; 28ms/page Heron-101) and Docling for IBM watsonx confirmed
- WebSearch: Firecrawl 2026 — /parse endpoint (May 2026; PDFs/Word/
  spreadsheets up to 50MB; 5× faster) confirmed from firecrawl.dev blog
- WebSearch: Chandra OCR / LightOn OCR / GLM-OCR / DeepSeek-OCR /
  HunyuanOCR 2026 — all confirmed still operating; no renames or pivots
- WebSearch: Qwen3-VL 2026 — confirmed current; 32-language OCR support
- WebSearch: Rossum / Docsumo / ABBYY / Kofax (Tungsten Automation)
  2026 — all confirmed operating
- WebSearch: Anthropic Claude document extraction 2026 — PDF support via
  Files API confirmed; no new dedicated document-extraction product
- WebSearch: OpenAI GPT-5 vision document 2026 — GPT-5.4 confirmed
  active for document understanding; no new extraction product
- WebSearch: Google Gemini 3.5 document OCR 2026 — Gemini 3.5 Flash
  (May 2026) confirmed; "Gemini 3.1 Pro" name appears in OmniDocBench
  rankings but relationship to "Gemini 3 Pro" in existing text could
  not be independently confirmed; existing text left unchanged
- WebSearch: xAI Grok vision document 2026 — multimodal capabilities
  present; no dedicated document-extraction product; no material change

**Material changes versus prior version (2026-05-31):**

- Added OCR-3 additional benchmark scores confirmed from official
  Nanonets X post: 87.4 on OLM-OCR (Global #1), 90.5 on OmniDocBench.
- Corrected Mistral OCR versioning: 25.05 is on Vertex AI (May 2026);
  25.03 remains on Azure AI Foundry. Removes the prior flagged
  uncertainty about "25.03 is the May 2026 update."
- Updated Reducto: Classification endpoint (May 2026) and Smart Schema
  (April 2026) added.
- Updated LlamaParse: ParseBench (April 2026) and Agentic Plus
  bounding-box visual grounding added.
- Updated Docling: Heron layout model (IBM Think 2026; 23.5% mAP; 28ms/
  page) and Docling for IBM watsonx enterprise platform added.
- Updated Firecrawl: /parse endpoint (May 2026; multi-format, 50MB
  limit, 5× speed) added; classification as "adjacent" unchanged.

---

**Date:** 2026-06-14

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 IDP leaderboard June 2026 ranking" —
  #1 at 85.9% confirmed; benchmarking.nanonets.com and
  idp-leaderboard.org URLs surfaced; ranking unchanged
- WebSearch: "site:huggingface.co/nanonets" — open-weight lineup
  unchanged (OCR-s, OCR2-3B, OCR2-1.5B-exp); OCR-3 remains API-only
- WebSearch: "nanonets arxiv 2026" — no team-authored papers surfaced;
  nanoindex (agentic RAG for long documents) noted but no arXiv paper
- WebSearch: Mistral OCR 2026 — Mistral OCR 3 pricing ($2/1,000 pages,
  50% batch discount) and 74% win rate over OCR 2 confirmed from
  VentureBeat and CloudPrice; Mistral OCR 2 retiring June 30, 2026
  confirmed from Xentoo blog (May 30, 2026 email)
- WebSearch: Reducto AI 2026 — no new June 2026 announcements; all
  prior entries (Series B, Deep Extract, Opennote, Classification,
  Smart Schema) confirmed current
- WebSearch: LlamaParse / LlamaIndex 2026 June — Parse-Flow launch
  (June 2026, visual document intelligence workflows) and ParseBench
  at CVPR 2026 confirmed from llamaindex.ai blog results; bounding-box
  granularity update confirmed
- WebSearch: Unstructured.io June 2026 — Microsoft Azure collaboration
  announced June 3, 2026 (Azure AI Search + Blob Storage pipelines)
  confirmed from multiple trade sources (HPC Wire, Yahoo Finance, etc.)
- WebSearch: Anthropic Claude document extraction June 2026 — Claude
  Fable 5 (June 9, 2026; claude-fable-5) and Claude Mythos 5 (limited
  availability, Project Glasswing) confirmed from Anthropic news and
  multiple review sites; advanced vision for diagrams/nested tables noted;
  ParseBench participation confirmed from LlamaIndex search results
- WebSearch: OpenAI GPT-5 document vision 2026 — GPT-5.4 (March 2026)
  and GPT-5.5 (April 2026) confirmed active; no new June 2026 models
- WebSearch: Google Gemini document OCR June 2026 — no major new
  announcement beyond Gemini 3.5 Flash already in context; Document AI
  OCR v2.1 migration recommended (minor)
- WebSearch: Chandra OCR / LightOn OCR / GLM-OCR / DeepSeek-OCR /
  HunyuanOCR / Qwen3-VL / Rossum / Docsumo / ABBYY / Kofax
  (Tungsten Automation) / Firecrawl 2026 — all confirmed operating;
  no renames, pivots, or closures since last refresh
- WebSearch: xAI Grok vision document 2026 — no new dedicated document
  extraction product; no change

**Material changes versus prior version (2026-06-07):**

- Added **Claude Fable 5** (June 9, 2026; claude-fable-5) and Claude
  Mythos 5 (limited availability) to the IDP Leaderboard comparables
  list and frontier-lab competitive-primary examples; Fable 5 includes
  advanced vision understanding for diagrams and nested tables and
  appears on ParseBench.
- Updated **Mistral OCR 3** entry: added confirmed pricing ($2/1,000
  pages; $1 with 50% batch discount), 74% win rate over OCR 2 in
  internal evaluations, and Mistral OCR 2 retirement by June 30, 2026.
- Updated **Unstructured.io** entry: added Microsoft Azure collaboration
  (June 3, 2026) covering Azure AI Search and Blob Storage pipelines
  for enterprise RAG and agentic workflows.
- Updated **LlamaParse** entry: added Parse-Flow (visual document
  intelligence workflows, June 2026) and ParseBench acceptance to
  CVPR 2026; word/line/cell-level bounding boxes confirmed.
- Nanonets OCR-3 #1 IDP Leaderboard ranking (85.9) confirmed
  unchanged. No new Nanonets-authored arXiv papers. No June 2026
  Nanonets blog posts indexed.

---

**Date:** 2026-06-21

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 IDP leaderboard June 2026 ranking" — #1 at
  85.9% confirmed unchanged; idp-leaderboard.org confirmed resolving
- WebSearch: "site:huggingface.co/nanonets" — open-weight model lineup
  unchanged (OCR-s, OCR2-3B, OCR2-1.5B-exp); OCR-3 remains API-only
- WebSearch: "nanonets arxiv 2026" — no team-authored papers surfaced;
  Nanonets-KIE appears as a benchmark dataset in Qianfan-OCR paper
- WebSearch: "Nanonets product announcement June 2026" — no new product
  announcements indexed; no Nanonets blog posts from June 2026
- WebFetch: `arxiv.org/abs/2603.13398` — Qianfan-OCR (Baidu Qianfan,
  March 2026; 4B params; 93.12 on OmniDocBench v1.5, 880 on OCRBench)
- WebSearch: "PaddleOCR-VL 1.6 OmniDocBench 2026" — PaddleOCR-VL-1.6
  (PaddlePaddle/Baidu, released May 28, 2026; technical report June 3,
  2026 arxiv 2606.03264; ~0.9B VLM; 96.33 on OmniDocBench v1.6, #1)
- WebSearch: "OmniDocBench v1.6 2026" — v1.6 released April 10, 2026
  (+296 pages, MGAM evaluation); v1.7 April 30, 2026 (Qianfan-OCR
  leaderboard added, skills-based evaluation)
- WebSearch: Mistral OCR 2026 June — no new model versions; minor API
  additions (table_format, extract_header/footer, hyperlinks output)
- WebSearch: Reducto AI 2026 June — AWS Marketplace availability
  (February 2026) confirmed; no new June 2026 announcements
- WebSearch: LlamaParse / LlamaIndex 2026 June — live webinar June 30;
  no new products beyond what's already in context
- WebSearch: Unstructured.io 2026 June — library v0.23.1 (June 11,
  2026); OpenSearch connectors added; no major product announcement
- WebSearch: Docling IBM 2026 June — Docling for IBM watsonx GA (June
  2026; $4/1,000 pages flat; 20% below comparable major vendors)
- WebSearch: GLM-OCR / Chandra OCR / LightOn OCR 2026 June — GLM-OCR
  now available in Azure AI Foundry alongside Chandra OCR 2; all
  confirmed operating
- WebSearch: Anthropic Claude document extraction June 2026 — no new
  document-specific product beyond Claude Fable 5 (already in context)
- WebSearch: OpenAI GPT-5 vision document June 2026 — GPT-5.4 and
  GPT-5.5 confirmed active; no new June 2026 models
- WebSearch: Google Gemini document OCR June 2026 — Gemini 3 Flash
  layout parser in Google Document AI (Preview); migration to later
  processor versions recommended before June 30, 2026
- WebSearch: xAI Grok document extraction June 2026 — Grok 4.3 on
  Amazon Bedrock (long-document workflows); Grok for Microsoft Word
  (document creation, not extraction); no dedicated document extraction
  product

**Material changes versus prior version (2026-06-14):**

- Added **Qianfan-OCR** (Baidu Qianfan, March 2026; 4B params; 93.12 on
  OmniDocBench v1.5; "Layout-as-Thought" architecture; open-weight on
  Hugging Face) to the competitive set alongside GLM-OCR, DeepSeek-OCR 2,
  HunyuanOCR.
- Added **PaddleOCR-VL-1.6** (PaddlePaddle/Baidu, released May 28, 2026;
  ~0.9B VLM; 96.33 on OmniDocBench v1.6, current #1 on that benchmark
  version) to the competitive set. Both Qianfan-OCR and PaddleOCR-VL-1.6
  could not be confirmed on the IDP Leaderboard (sites 403); added to
  competitive set only, not to the IDP Leaderboard comparables list.
- Removed "tops that benchmark" qualifier from GLM-OCR entry; GLM-OCR
  remains #1 on OmniDocBench v1.5 (94.62) but PaddleOCR-VL-1.6 leads
  the v1.6 edition (96.33); scores across versions are not comparable.
- Added note on OmniDocBench versioning: v1.6 (April 10, 2026) and v1.7
  (April 30, 2026) now exist; v1.5-based scores in prior context remain
  accurate for their benchmark version.
- Updated **Docling for IBM watsonx** entry to note general availability
  (June 2026; $4/1,000 pages flat pricing, 20% below "selected major
  vendors" per IBM list pricing).
- Nanonets OCR-3 #1 IDP Leaderboard ranking (85.9) confirmed unchanged.
  No new Nanonets models on Hugging Face. No Nanonets-authored arXiv
  papers found.

---

**Date:** 2026-06-28

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 IDP leaderboard June 2026 ranking" —
  #1 at 85.9% confirmed unchanged; idp-leaderboard.org and
  benchmarking.nanonets.com both resolving
- WebSearch: "site:huggingface.co/nanonets" — open-weight model lineup
  unchanged (OCR-s, OCR2-3B, OCR2-1.5B-exp); OCR-3 remains API-only
- WebSearch: "nanonets arxiv 2026 research paper" — no team-authored
  papers surfaced; Nanonets-KIE dataset referenced in Qianfan-OCR paper
  (as in prior refresh)
- WebSearch: "Mistral OCR 2026 June update pricing model" — Mistral OCR
  4 (June 23, 2026; mistral-ocr-4-0) confirmed from mistral.ai/news/ocr-4
  and multiple trade sources (VentureBeat, MarkTechPost, TechTimes)
- WebSearch: `"Mistral OCR 4" features bounding boxes model ID pricing` —
  model ID, pricing ($4/$2 batch), OlmOCRBench (85.20), 72% win rate,
  170 languages, self-hosted container confirmed
- WebSearch: "Baidu Unlimited OCR" June 2026 — Unlimited-OCR (June 22,
  2026; arXiv 2606.23050; 3B MoE, R-SWA, MIT license) confirmed from
  MarkTechPost, Pandaily, Medium, and GitHub repo
- WebSearch: "Surya 2 OCR 2026 benchmark release" — Surya OCR 2 (Datalab,
  May 27, 2026; 650M; OlmOCR-bench 83.3%; 91 languages) confirmed from
  datalab.to blog and HuggingFace
- WebSearch: "Reducto AI 2026 June" — no new June announcements; all
  prior entries confirmed current
- WebSearch: "LlamaParse LlamaIndex 2026 June" — no new products beyond
  what's in context; June 30 webinar noted
- WebSearch: "Unstructured.io 2026 June" — library v0.23.1 only;
  no new product announcement
- WebSearch: "Docling IBM 2026 June" — docling-ibm-models PyPI package
  (June 4, 2026); Docling for watsonx GA confirmed
- WebSearch: "Chandra OCR LightOn OCR 2026 June" — no new model
  versions; both confirmed operating
- WebSearch: "Anthropic Claude document extraction vision June 2026" —
  Claude Opus 4.7 (April 16, 2026; 2,576px max image, 3× prior models)
  confirmed from Anthropic news and Amazon Bedrock announcement
- WebSearch: "Claude Opus 4.7 vision document features" — improved
  chart and document parsing accuracy confirmed from MindStudio and
  Claudefa.st reviews
- WebSearch: "OpenAI GPT-5 document vision OCR June 2026" — GPT-5.4
  and GPT-5.5 confirmed active; no new June 2026 models
- WebSearch: "Google Gemini document OCR vision June 2026" — Gemini 3
  Pro vision confirmed; Gemini Document AI layout parser (OCR + Gemini)
  in general use; no major new June announcement
- WebSearch: "xAI Grok Collections API OCR document extraction 2026" —
  Grok Collections API confirmed (OCR+layout parsing for PDF/Excel
  indexing; $2.50/1,000 searches) from x.ai/news and xAI docs
- WebSearch: "Rossum Docsumo ABBYY Kofax Tungsten Automation 2026" —
  all confirmed operating; Rossum (Coupa), ABBYY Vantage, Docsumo,
  Tungsten Automation all actively marketed in 2026
- WebSearch: "Firecrawl 2026 June document AI update" — Research Index
  (June 16, 2026; 3M+ arXiv papers) confirmed; /parse endpoint and
  Rust engine from prior context still current

**Material changes versus prior version (2026-06-21):**

- Updated **Mistral OCR** entry: Mistral OCR 4 (June 23, 2026;
  model ID mistral-ocr-4-0; mistral-ocr-latest now points to this)
  adds bounding boxes, typed-block labels, per-word confidence scores,
  170-language self-hosted container; $4/1K pages ($2 batch); 85.20
  OlmOCRBench; 72% win rate. Supersedes Mistral OCR 3. Mistral OCR 2
  confirmed retired June 30, 2026.
- Added **Unlimited-OCR** (Baidu, June 22, 2026; 3B MoE, R-SWA constant
  KV cache for long-document single-pass parsing; 93.23 OmniDocBench
  v1.5, 93.92 v1.6; MIT license; arXiv 2606.23050) to competitive set.
- Added **Surya OCR 2** (Datalab, May 27, 2026; 650M params; same team
  as Chandra OCR 2; 83.3% OlmOCR-bench; 91 languages; Apache 2.0) to
  competitive set.
- Updated frontier-lab competitive examples: added Claude Opus 4.7
  (April 16, 2026; 2,576px max image resolution, 3× prior models;
  improved document parsing) alongside Fable 5; added Grok Collections
  API (OCR+layout-aware parsing for document RAG) to xAI entry.
- Nanonets OCR-3 #1 IDP Leaderboard ranking (85.9) confirmed
  unchanged. No new Nanonets models on Hugging Face. No
  Nanonets-authored arXiv papers found.

---

**Date:** 2026-07-05

**Sources consulted:**

- `nanonets.com`, `nanonets.com/blog`, `benchmarking.nanonets.com`,
  `idp-leaderboard.org` — all returned HTTP 403; fell back to web
  search for all Nanonets data
- WebSearch: "Nanonets OCR-3 IDP leaderboard July 2026 ranking" —
  #1 at 85.9% confirmed unchanged; idp-leaderboard.org and
  benchmarking.nanonets.com URLs confirmed resolving
- WebSearch: "site:huggingface.co/nanonets" — open-weight model lineup
  unchanged (OCR-s, OCR2-3B, OCR2-1.5B-exp); OCR-3 remains API-only
- WebSearch: "nanonets arxiv 2026 research paper" — no team-authored
  papers surfaced; Nanonets-KIE dataset referenced in third-party
  papers (as in prior refreshes)
- WebSearch: "Nanonets OCR-3 new announcement product July 2026" —
  no new Nanonets product announcements in July 2026
- WebSearch: "Mistral OCR July 2026 new model update" — no new model
  since Mistral OCR 4 (June 23, 2026); July 7 webinar scheduled;
  all prior entries confirmed current
- WebSearch: "Reducto LongExtractBench date announcement July 2026"
  + "Reducto LongExtractBench" — LongExtractBench (July 1, 2026;
  micro1-audited; 225 documents; Reducto Deep Extract #1) confirmed
  from PRNewswire, reducto.ai blog, TipRanks, LinkedIn (micro1 post)
- WebSearch: "Extend AI Extend MAX document processing funding 2026"
  — Extend confirmed as YC-backed startup (extend.ai); $17M raised;
  appeared as peer in LongExtractBench as "Extend MAX"
- WebSearch: "LlamaParse LlamaIndex July 2026 new product" — no new
  July 2026 products beyond what's in context; LlamaCloud rebranding
  confirmed; LiteParse and Parse-Flow unchanged
- WebSearch: "Unstructured.io July 2026 new update" — library v0.18.11
  (July 23) and unstructured-api v0.0.89 (July 5, CVE patch); no
  material product announcement
- WebSearch: "Docling IBM July 2026 update release" — docling-parse v6
  (threaded PDF parser, worker thread pool) released mid-2026; Docling
  for IBM watsonx GA already in context; no additional major announcement
- WebSearch: "Firecrawl July 2026 document parsing update" — PDF upload
  limit raised (minor operational change); Fire-PDF and /parse endpoint
  already in context; no major new feature
- WebSearch: "Claude Opus 4.8 Anthropic release document vision 2026"
  — Opus 4.8 (May 28, 2026) confirmed from Anthropic news,
  artificialintelligence-news.com, MacRumors; focus: dynamic
  multi-agent workflows; appears in LongExtractBench (July 2026)
- WebSearch: "Gemini 3.1 Pro Google release date 2026" — Gemini 3.1
  Pro (February 19, 2026) confirmed from Google DeepMind blog and
  Google Cloud docs; distinct model from "Gemini 3 Pro"; appears in
  LongExtractBench comparisons
- WebSearch: "Anthropic Claude document extraction vision July 2026"
  — no new Anthropic document-specific product beyond what's in context
- WebSearch: "OpenAI GPT-5 document vision OCR July 2026" — GPT-5.4
  and GPT-5.5 confirmed active; no new July 2026 models
- WebSearch: "Google Gemini document OCR vision July 2026" — Gemini 3
  Pro confirmed as frontier vision model; no major new July announcement
- WebSearch: "xAI Grok document extraction OCR July 2026" — Grok
  Collections API confirmed unchanged from prior context
- WebSearch: "DeepSeek OCR VLM new model July 2026" — no new model
  since DeepSeek-OCR 2 (January 2026); confirmed unchanged
- WebSearch: "Qwen3-VL Qwen VLM new release July 2026" — Qwen3-VL
  confirmed current; Qwen3-VL-Embedding (embedding variant) noted
  but not directly relevant to document extraction product surface
- WebSearch: "new OCR VLM model document AI July 2026" — no new
  entrants beyond Extend (already captured above)

**Material changes versus prior version (2026-06-28):**

- Added **Extend** (extend.ai; YC-backed; $17M raised) to the
  competitive set as a new entrant. Appeared as a direct peer in
  LongExtractBench (July 2026) alongside Reducto, LlamaExtract-Agentic,
  GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro. Positions as
  end-to-end "document processing cloud."
- Updated **Reducto**: added LongExtractBench #1 result (July 1, 2026;
  micro1-audited; 225 documents; 100% completeness, 99.6% precision,
  99.6% recall, 99.3% leaf accuracy; zero failures).
- Added **Claude Opus 4.8** (May 28, 2026) to the frontier-lab
  competitive-primary Anthropic example and IDP Leaderboard comparables
  list; dynamic multi-agent workflows; evaluated on LongExtractBench.
- Added **Gemini 3.1 Pro** (February 19, 2026) to the Google frontier-lab
  example and IDP Leaderboard comparables list; distinct from "Gemini 3
  Pro" and older than Gemini 3.5 Flash; appears in LongExtractBench.
- Nanonets OCR-3 #1 IDP Leaderboard ranking (85.9) confirmed unchanged.
  No new Nanonets models on Hugging Face. No Nanonets-authored arXiv
  papers found. No July 2026 Nanonets blog posts indexed.
