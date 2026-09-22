from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ResearchProject:
    project_id: str
    title: str
    question: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "created"

@dataclass
class ResearchResult:
    project_id: str
    answer: str
    confidence: float
    citations: list[str]
    warnings: list[str] = field(default_factory=list)
