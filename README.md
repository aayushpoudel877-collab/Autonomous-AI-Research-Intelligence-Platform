# NEXUS — Autonomous AI Research & Intelligence Platform

NEXUS is a modular research intelligence platform for ingesting heterogeneous evidence, indexing knowledge, retrieving relevant context, building a lightweight knowledge graph, verifying claims, forecasting numeric series, and orchestrating research workflows through specialized agents.

## Architecture

`Sources → Ingestion → Normalization → Chunking → Embeddings → Retrieval → Knowledge Graph → Agents → Verification/Forecasting → Evidence-backed Report`

The repository is intentionally provider-agnostic: local deterministic components work without API keys, while adapters can be added for production LLM, vector, graph, and web providers.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -e '.[dev]'
uvicorn nexus.api.main:app --reload
```

Open `/docs` for the API explorer and `/` for the lightweight dashboard.

## Design goals
- Evidence first: every generated insight can point back to source chunks.
- Deterministic local baseline: useful development without paid APIs.
- Replaceable adapters for embeddings, LLMs, search, graph stores and observability.
- Testable agent orchestration instead of a monolithic prompt.
- Security-conscious boundaries and explicit provenance.

## Roadmap
The repository is organized as a long-running engineering project with incremental architecture, data, AI, verification, MLOps, security, testing, and deployment milestones.

## Phase 2: Web ingestion and persistence

The platform now supports a safer research-ingestion path for public HTTP(S) pages. URL ingestion validates the destination host, rejects private/loopback/link-local/reserved networks, enforces a response-size limit, strips executable HTML sections, and converts readable page content into the same normalized chunk pipeline used by local text.

The API now accepts typed ingestion sources:

- `POST /api/v1/ingest` with `{"source_type":"text","text":"..."}`
- `POST /api/v1/ingest` with `{"source_type":"url","text":"https://example.org"}`
- `POST /api/v1/research` with `{"question":"...","top_k":10}`

Indexed chunks are persisted in SQLite and hydrated into the semantic retriever when the application starts, so a process restart no longer discards the research corpus.

This phase intentionally keeps external web fetching bounded and synchronous. A future worker layer will add retries, canonicalization, robots/policy controls, PDF extraction, async jobs, and distributed storage.

## Phase 3: Research acquisition and evidence intelligence

NEXUS now extends the acquisition layer beyond plain text and HTML. Local PDF documents can be parsed into page-aware text, bounded by an ingestion-size policy, and sent through the same normalization/chunking/indexing pipeline.

Retrieval now uses a hybrid score combining deterministic semantic embeddings with token-level lexical relevance. This improves exact-term matching while retaining semantic retrieval behavior.

Research reports expose stable evidence identifiers such as `[E1]` and return citation metadata containing the originating source URI and retrieval score. Provenance utilities also provide deterministic SHA-256 content hashes for audit trails.

### Phase 3 source matrix

| Source | Adapter | Persistence | Retrieval | Provenance |
|---|---|---|---|---|
| Inline text | Yes | Yes | Hybrid | Yes |
| Public HTML | Yes | Yes | Hybrid | Yes |
| Local PDF | Yes | Yes | Hybrid | Yes |

The next phase can build on this foundation with asynchronous acquisition jobs, richer PDF metadata/layout extraction, persistent vector indexes, entity-aware graph retrieval, model-provider routing, and stronger citation verification.


## Phase 4: Knowledge intelligence

NEXUS now turns retrieved evidence into a provenance-aware knowledge graph before verification. Entity and relation extraction is deterministic and provider-free, while graph edges retain the originating chunk and source URI. Graph retrieval expands one or two hops from entities mentioned by the research question, enabling lightweight multi-hop evidence traversal.

Verification now checks citation IDs against the actual evidence set and detects graph-level conflicts where the same subject/relation points to different targets. Research responses expose citation-integrity metadata, contradiction findings, and graph-fact counts. This keeps the intelligence layer auditable rather than presenting graph-derived statements as unsupported model output.

### Phase 4 flow

Question → Hybrid Retrieval → Entity/Relation Extraction → Graph Expansion → Contradiction Detection → Citation Verification → Report

The graph implementation is intentionally deterministic and replaceable. Future phases can add persistent graph storage, entity linking against external knowledge bases, richer relation models, asynchronous acquisition, and model-provider routing without changing the agent contract.


## Phase 5: Autonomous research orchestration

The research layer now performs bounded autonomous planning over the indexed evidence corpus. A deterministic planner decomposes a research question into a small set of auditable subquestions, and the retrieval agent executes those planned queries before graph expansion and verification. This avoids hiding autonomous behavior inside an opaque prompt while preserving the existing agent contract.

Research memory is persisted in SQLite, including the question, generated plan, evidence count, graph-fact count, and citation-integrity measurement. The knowledge graph is also persisted and rehydrated at startup, fixing the previous process-local graph limitation.

Source discovery now groups retrieved evidence by originating source URI and ranks sources by their strongest retrieval score. The API exposes the research plan, iteration count, discovered sources, graph facts, contradictions, and citation-integrity information. The bounded loop is intentionally local and deterministic; external search providers can be added later through a replaceable discovery adapter.

### Phase 5 flow

Question → Research Planner → Planned Retrieval → Source Discovery → Knowledge Graph → Verification → Citation Audit → Research Memory → Report


## Phase 6: External research acquisition and multi-source intelligence

Phase 6 closes the gap between autonomous research planning and actual source acquisition. The research layer now has a replaceable `SourceSearchProvider` contract, deterministic caller-supplied URL discovery, URL canonicalization, transparent source-quality scoring, content deduplication, persisted acquisition metadata, bounded parallel fetching, and an in-process asynchronous job manager.

The acquisition path deliberately separates network I/O from corpus mutation: URLs are fetched concurrently, then accepted documents are indexed sequentially. This prevents worker-thread races in the in-memory hybrid retriever while still reducing acquisition latency.

### Phase 6 capabilities

- Canonical HTTP(S) URLs with tracking-parameter removal.
- Provider interface for future search-engine/news/database adapters.
- Deterministic `StaticURLProvider` for API-driven or test-driven source lists.
- Source quality heuristic with explicit, bounded scoring rather than an opaque ranking.
- SHA-256 normalized content deduplication.
- Persisted source metadata: canonical URL, provider, quality, content hash, fetch time, and freshness value.
- Bounded concurrent web acquisition with per-source failure isolation.
- Synchronous acquisition integrated directly into `POST /api/v1/research`.
- Asynchronous acquisition jobs through `POST /api/v1/research/acquire` and `GET /api/v1/research/acquire/{job_id}`.
- Acquired-source inspection through `GET /api/v1/research/sources`.
- Duplicate chunk protection in the hybrid retriever.

### Phase 6 research flow

Question → Planner → Source Candidates → Safe Web Acquisition → Canonicalization/Deduplication → Quality/Freshness Metadata → Persistent Index → Planned Retrieval → Knowledge Graph → Verification → Report

The search-provider boundary remains intentionally provider-agnostic. No commercial search API is hard-coded into the repository, so a production provider can be added without changing the research controller or agent contracts.
