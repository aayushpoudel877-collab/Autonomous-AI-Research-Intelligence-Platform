class SessionMemory:
    def __init__(self): self.items=[]
    def remember(self,item): self.items.append(item)
    def recent(self,n=10): return self.items[-n:]
