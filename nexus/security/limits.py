def validate_text_size(text:str,max_chars:int)->None:
    if len(text)>max_chars: raise ValueError(f'text exceeds {max_chars} characters')
