from urllib.parse import urlsplit

def host(uri:str)->str:
    return urlsplit(uri).netloc.lower()
