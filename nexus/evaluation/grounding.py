def grounded(evidence_count:int,confidence:float)->bool:
    return evidence_count>0 and confidence>=0.5
