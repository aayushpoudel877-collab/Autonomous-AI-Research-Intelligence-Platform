from typing import Literal
from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_type: Literal["text", "url", "pdf"] = "text"
    text: str | None = None
    title: str = "Text Input"


class ResearchRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)
    graph_hops: int = Field(default=1, ge=1, le=2)
    max_iterations: int = Field(default=3, ge=1, le=3)


class ResearchResponse(BaseModel):
    question: str
    report: str
    evidence_count: int
    grounded: bool
    citations: list[dict[str, str | float]] = Field(default_factory=list)
    citation_integrity: dict = Field(default_factory=dict)
    contradictions: list[dict] = Field(default_factory=list)
    graph_fact_count: int = 0
    research_plan: list[str] = Field(default_factory=list)
    iterations: int = 0
    discovered_sources: list[dict[str, str | float]] = Field(default_factory=list)
