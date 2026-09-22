import re

def detect_language(text: str) -> str:
    if re.search(r"[\u0900-\u097F]", text): return "ne"
    return "en"
