# Architecture

NEXUS follows ports-and-adapters principles. Ingestion produces normalized `SourceDocument` objects. Chunking creates stable evidence units. Embedding and retrieval are replaceable. Agents operate on an explicit `AgentContext`, making orchestration observable and testable. Verification and reporting are downstream of retrieval so unsupported claims can be flagged.

## Production evolution
1. Replace in-memory retrieval with a vector database.
2. Add a graph database adapter.
3. Add signed source provenance and crawl policies.
4. Add model gateway with provider failover.
5. Add distributed workers and event streaming.
