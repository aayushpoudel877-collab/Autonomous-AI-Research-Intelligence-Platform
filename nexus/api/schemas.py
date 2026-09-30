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
    source_urls: list[str] = Field(default_factory=list, max_length=20)
    max_sources: int = Field(default=5, ge=1, le=20)
    target_evidence: int = Field(default=5, ge=1, le=20)
    target_sources: int = Field(default=2, ge=1, le=10)
    min_average_score: float = Field(default=0.15, ge=0.0, le=1.0)
    max_age_days: float = Field(default=1.0, ge=0.0, le=30.0)
    force_refresh: bool = False


class AcquisitionRequest(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=20)
    max_sources: int = Field(default=5, ge=1, le=20)


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
    acquisition: dict = Field(default_factory=dict)
    evidence_assessment: dict = Field(default_factory=dict)


class AcquisitionJobResponse(BaseModel):
    job_id: str
    status: str
    error: str = ""
    result: dict | None = None
