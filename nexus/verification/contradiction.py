def detect_conflict(a: str, b: str) -> bool:
    neg={"not","never","no","false","cannot"}
    return bool((set(a.lower().split()) & neg) ^ (set(b.lower().split()) & neg))
