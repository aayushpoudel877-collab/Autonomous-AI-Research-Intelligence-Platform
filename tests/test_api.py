from fastapi.testclient import TestClient
from nexus.api.main import app
client=TestClient(app)

def test_health(): assert client.get('/api/v1/health').json()['status']=='ok'

def test_research_flow():
    client.post('/api/v1/ingest',json={'text':'NEXUS is a research intelligence platform.'})
    r=client.post('/api/v1/research',json={'question':'What is NEXUS?'})
    assert r.status_code==200 and r.json()['evidence_count']>=1
