def mae(actual,predicted):
    if not actual: return 0.0
    return sum(abs(a-p) for a,p in zip(actual,predicted))/len(actual)
