import argparse
from nexus.ingestion.text import TextIngestor
from nexus.pipeline.index import IndexPipeline
from nexus.pipeline.research import build_orchestrator

def main():
    p=argparse.ArgumentParser(); p.add_argument('question'); p.add_argument('--evidence',default=''); a=p.parse_args()
    pipeline=IndexPipeline();
    if a.evidence: pipeline.index([TextIngestor().ingest(a.evidence)])
    result=build_orchestrator(pipeline.retriever).run(a.question); print(result.state['report'])

if __name__=='__main__': main()
