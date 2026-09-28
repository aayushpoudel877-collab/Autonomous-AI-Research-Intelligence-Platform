from fastapi import APIRouter, HTTPException

from nexus.api.dependencies import retriever, store
from nexus.api.schemas import IngestRequest, ResearchRequest, ResearchResponse
from nexus.ingestion.registry import get_ingestor
from nexus.pipeline.index import IndexPipeline
from nexus.pipeline.research import build_orchestrator

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "nexus", "indexed_chunks": len(retriever.items)}


@router.post("/ingest")
def ingest(request: IngestRequest):
    if not request.text:
        raise HTTPException(status_code=422, detail="text must contain source content or a file path")
    try:
        doc = get_ingestor(request.source_type).ingest(request.text)
        if request.source_type == "text" and request.title != "Text Input":
            doc.title = request.title
        chunks = IndexPipeline(retriever, store=store).index([doc])
        return {"document_id": doc.document_id, "chunks": len(chunks), "source_uri": doc.source_uri, "metadata": doc.metadata}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    ctx = build_orchestrator(retriever).run(request.question, top_k=request.top_k, graph_hops=request.graph_hops)
    verification = ctx.state["verification"]
    return ResearchResponse(
        question=request.question,
        report=ctx.state["report"],
        evidence_count=verification["evidence_count"],
        grounded=verification["grounded"],
        citations=ctx.state.get("citations", []),
        citation_integrity=verification.get("citation_integrity", {}),
        contradictions=verification.get("contradictions", []),
        graph_fact_count=len(ctx.state.get("graph_facts", [])),
    )
