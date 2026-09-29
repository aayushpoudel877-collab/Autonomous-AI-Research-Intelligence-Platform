from collections import Counter
import math
import re

_TOKEN = re.compile(r"\b[\w-]+\b", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def lexical_score(query: str, text: str) -> float:
    q = Counter(_tokens(query))
    t = Counter(_tokens(text))
    dot = sum(q[k] * t[k] for k in q)
    nq = math.sqrt(sum(v * v for v in q.values()))
    nt = math.sqrt(sum(v * v for v in t.values()))
    return dot / (nq * nt) if nq and nt else 0.0
