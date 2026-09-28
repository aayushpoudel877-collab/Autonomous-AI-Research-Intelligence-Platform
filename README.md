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
