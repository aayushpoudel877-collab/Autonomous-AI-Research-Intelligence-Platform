from collections import Counter
import math

def lexical_score(query: str, text: str) -> float:
    q=Counter(query.lower().split()); t=Counter(text.lower().split())
    dot=sum(q[k]*t[k] for k in q); nq=math.sqrt(sum(v*v for v in q.values())); nt=math.sqrt(sum(v*v for v in t.values()))
    return dot/(nq*nt) if nq and nt else 0.0
