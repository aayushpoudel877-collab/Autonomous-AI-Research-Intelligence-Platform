def mix(parts:dict[str,float],weights:dict[str,float])->float:
    return sum(parts.get(k,0.0)*weights.get(k,0.0) for k in weights)
