def trim(text:str,limit:int)->str:
    return text if len(text)<=limit else text[:max(0,limit-1)]+'…'
