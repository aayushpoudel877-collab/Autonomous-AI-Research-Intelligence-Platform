def score_gap(scores:list[float])->float:
    return scores[0]-scores[1] if len(scores)>1 else (scores[0] if scores else 0.0)