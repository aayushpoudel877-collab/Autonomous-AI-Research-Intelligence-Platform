import re

def sections(text:str)->list[tuple[str,str]]:
    parts=re.split(r"(?m)^#{1,3}\s+(.+)$",text)
    return [(parts[i].strip(),parts[i+1].strip()) for i in range(1,len(parts)-1,2)]
