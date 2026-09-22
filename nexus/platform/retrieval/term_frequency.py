from collections import Counter
def counts(text:str)->dict[str,int]:return dict(Counter(text.lower().split()))