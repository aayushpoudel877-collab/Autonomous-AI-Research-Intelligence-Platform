from .text_cleaner import clean_text
from .markdown import strip_markdown

def normalize(text:str)->str:
    return clean_text(strip_markdown(text))
