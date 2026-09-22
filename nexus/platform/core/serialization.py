import json
from dataclasses import asdict, is_dataclass


def to_json(value: object) -> str:
    payload = asdict(value) if is_dataclass(value) else value
    return json.dumps(payload, sort_keys=True, default=str)
