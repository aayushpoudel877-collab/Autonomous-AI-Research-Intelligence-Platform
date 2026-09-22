from fastapi import APIRouter
from nexus.api.dependencies import retriever
from nexus.api.schemas import IngestRequest, ResearchRequest, ResearchResponse
from nexus.pipeline.index import IndexPipeline
from nexus.pipeline.research import build_orchestrator
from nexus.types import SourceDocument
from nexus.utils import stable_id

router=APIRouter()

@router.get('/health')
def health(): return {'status':'ok','service':'nexus'}

@router.post('/ingest')
def ingest(request: IngestRequest):
    doc=SourceDocument(stable_id(request.title,request.text),request.title,request.text,'api')
    chunks=IndexPipeline(retriever).index([doc])
    return {'document_id':doc.document_id,'chunks':len(chunks)}

@router.post('/research',response_model=ResearchResponse)
def research(request: ResearchRequest):
    ctx=build_orchestrator(retriever).run(request.question)
    verification=ctx.state['verification']
    return ResearchResponse(question=request.question,report=ctx.state['report'],evidence_count=verification['evidence_count'],grounded=verification['grounded'])
