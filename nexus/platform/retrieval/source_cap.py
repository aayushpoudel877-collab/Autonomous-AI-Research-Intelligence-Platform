def cap_by_source(items:list[tuple[str,str]],cap:int)->list[tuple[str,str]]:
    seen={};out=[]
    for item,source in items:
        if seen.get(source,0)<cap:out.append((item,source));seen[source]=seen.get(source,0)+1
    return out