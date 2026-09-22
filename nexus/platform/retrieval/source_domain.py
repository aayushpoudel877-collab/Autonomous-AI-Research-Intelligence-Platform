def source_domain(uri:str)->str:
    return uri.split('/')[2].lower() if '://' in uri else uri.lower()
