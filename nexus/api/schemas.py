from typing import Literal
from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_type: Literal["text", "url"] = "text"
    text: str | None = None
    title: str = "Text Input"


class ResearchRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


class ResearchResponse(BaseModel):
    question: str
    report: str
    evidence_count: int
    grounded: bool
