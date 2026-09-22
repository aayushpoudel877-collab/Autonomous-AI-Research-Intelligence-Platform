def validate_text(text:str,min_chars:int=1)->str:
    value=text.strip()
    if len(value)<min_chars: raise ValueError("text does not meet minimum length")
    return value
