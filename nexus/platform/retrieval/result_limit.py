def limit_results(items:list[object],limit:int)->list[object]:
    return items[:max(0,limit)]
