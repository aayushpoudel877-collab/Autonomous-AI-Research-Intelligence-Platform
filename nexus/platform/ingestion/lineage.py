from dataclasses import dataclass
@dataclass(frozen=True)
class Lineage:
    source_id:str
    parent_id:str|None=None
    transform:str="ingest"
