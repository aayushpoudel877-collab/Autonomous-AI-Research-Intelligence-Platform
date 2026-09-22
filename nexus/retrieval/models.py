from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float = Field(ge=-1, le=1)
    source_uri: str
