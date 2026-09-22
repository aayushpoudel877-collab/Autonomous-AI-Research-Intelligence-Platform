def variance(scores:list[float])->float:
    if not scores:return 0.0
    mean=sum(scores)/len(scores)
    return sum((x-mean)**2 for x in scores)/len(scores)