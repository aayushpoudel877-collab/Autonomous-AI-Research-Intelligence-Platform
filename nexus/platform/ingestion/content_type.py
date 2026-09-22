def classify(text:str)->str:
    if text.lstrip().startswith("{"): return "json-like"
    if text.lstrip().startswith("#"): return "markdown-like"
    return "plain-text"
