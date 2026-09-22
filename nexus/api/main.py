from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nexus.api.routes import router
from nexus.config import get_settings
from nexus.logging import configure_logging

configure_logging()
settings=get_settings()
app=FastAPI(title=settings.app_name,version='0.1.0')
app.include_router(router,prefix='/api/v1')

@app.get('/',response_class=HTMLResponse)
def dashboard():
    return '''<!doctype html><html><head><title>NEXUS</title><style>body{font-family:system-ui;max-width:900px;margin:50px auto;padding:20px}textarea{width:100%;height:140px}button{padding:10px 18px}pre{white-space:pre-wrap}</style></head><body><h1>NEXUS</h1><p>Autonomous AI Research & Intelligence Platform</p><textarea id="q" placeholder="Enter research evidence or question"></textarea><br><button onclick="run()">Research</button><pre id="o"></pre><script>async function run(){const q=document.getElementById('q').value;const r=await fetch('/api/v1/ingest',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:q})});await r.json();const x=await fetch('/api/v1/research',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});document.getElementById('o').textContent=JSON.stringify(await x.json(),null,2)}</script></body></html>'''
