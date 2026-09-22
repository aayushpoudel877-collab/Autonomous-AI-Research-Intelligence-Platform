# API

`GET /api/v1/health` — service health.

`POST /api/v1/ingest` — index text evidence. Body: `{text,title}`.

`POST /api/v1/research` — run the local research workflow. Body: `{question,top_k}`.

Swagger/OpenAPI is available at `/docs` when the service is running.
