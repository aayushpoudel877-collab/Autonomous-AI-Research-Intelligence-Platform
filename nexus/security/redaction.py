import re
EMAIL=re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
def redact(text:str)->str: return EMAIL.sub('[REDACTED_EMAIL]',text)
