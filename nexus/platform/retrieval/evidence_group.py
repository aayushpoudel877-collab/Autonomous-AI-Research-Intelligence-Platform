from dataclasses import dataclass
@dataclass(frozen=True)
class EvidenceGroup:
    source:str
    item_ids:tuple[str,...]
