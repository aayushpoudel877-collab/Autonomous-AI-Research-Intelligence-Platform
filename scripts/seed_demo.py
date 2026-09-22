from nexus.ingestion.text import TextIngestor
from nexus.pipeline.index import IndexPipeline

def main():
    docs=[
      'NEXUS combines retrieval, knowledge graphs, verification, and forecasting.',
      'Evidence-backed research systems should preserve source provenance.',
      'Hybrid retrieval can combine lexical and semantic signals.'
    ]
    pipeline=IndexPipeline(); pipeline.index([TextIngestor().ingest(x) for x in docs]); print('Demo corpus indexed.')
if __name__=='__main__': main()
