import re

def infer_title(text:str,max_chars:int=80)->str:
    first=next((line.strip() for line in text.splitlines() if line.strip()),"Untitled")
    return re.sub(r"^#+\s*","",first)[:max_chars]
