from fastapi import APIRouter, HTTPException

from nexus.api.dependencies import graph, retriever, store
from nexus.api.schemas import (
    AcquisitionJobResponse,
    AcquisitionRequest,
    IngestRequest,
    ResearchRequest,
    ResearchResponse,
)
from nexus.ingestion.registry import get_ingestor
from nexus.pipeline.index import IndexPipeline
from nexus.pipeline.research import build_orchestrator
from nexus.research.acquisition import AcquisitionManager
from nexus.research.controller import ResearchAcquisitionController
from nexus.research.engine import AutonomousResearchEngine
from nexus.research.jobs import ResearchJobManager
from nexus.research.memory import ResearchMemoryStore
from nexus.research.providers import StaticURLProvider

router = APIRouter()
job_manager = ResearchJobManager()


def _acquisition_manager():
    return AcquisitionManager(IndexPipeline(retriever, store=store), storage=store)


def _acquire_urls(urls, max_sources):
    provider = StaticURLProvider(urls)
    result = _acquisition_manager().acquire(provider.search("", limit=max_sources), max_sources=max_sources)
    return {
        "requested": result.requested,
        "acquired": result.acquired,
        "skipped": result.skipped,
        "failed": result.failed,
        "sources": [source.__dict__ for source in result.sources],
        "errors": list(result.errors),
    }


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
    engine = AutonomousResearchEngine(
        retriever, lambda: build_orchestrator(retriever, graph), ResearchMemoryStore(store)
    )
    controller = ResearchAcquisitionController(engine, _acquisition_manager())
    ctx = controller.run(
        request.question,
        source_urls=request.source_urls,
        max_sources=request.max_sources,
        top_k=request.top_k,
        graph_hops=request.graph_hops,
        max_iterations=request.max_iterations,
    )
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
        research_plan=ctx.state.get("research_plan", []),
        iterations=ctx.state.get("iterations", 0),
        discovered_sources=ctx.state.get("discovered_sources", []),
        acquisition=ctx.state.get("acquisition", {}),
    )


@router.post("/research/acquire", response_model=AcquisitionJobResponse)
def acquire(request: AcquisitionRequest):
    job = job_manager.submit(_acquire_urls, request.urls, request.max_sources)
    return AcquisitionJobResponse(job_id=job.job_id, status=job.status)


@router.get("/research/acquire/{job_id}", response_model=AcquisitionJobResponse)
def acquisition_job(job_id: str):
    job = job_manager.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Acquisition job not found")
    return AcquisitionJobResponse(job_id=job.job_id, status=job.status, error=job.error, result=job.result)


@router.get("/research/memory")
def research_memory(limit: int = 10):
    limit = max(1, min(limit, 50))
    return {"items": [m.__dict__ for m in ResearchMemoryStore(store).recent(limit)]}


@router.get("/research/sources")
def research_sources(limit: int = 20):
    limit = max(1, min(limit, 100))
    return {"items": store.load_acquired_sources(limit)}
