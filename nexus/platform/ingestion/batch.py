from dataclasses import dataclass
@dataclass
class BatchResult:
    accepted:int=0
    rejected:int=0
    warnings:list[str]|None=None
    def __post_init__(self): self.warnings=[] if self.warnings is None else self.warnings
