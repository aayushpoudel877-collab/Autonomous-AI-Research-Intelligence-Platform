from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class AgentContext:
    question: str
    evidence: list = field(default_factory=list)
    state: dict = field(default_factory=dict)

class Agent(ABC):
    name="base"
    @abstractmethod
    def run(self, context: AgentContext) -> AgentContext: ...
