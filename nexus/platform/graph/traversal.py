from collections import deque
def bfs(store,start,depth=2):
    seen={start};q=deque([(start,0)]);out=[]
    while q:
        node,d=q.popleft()
        if d>=depth:continue
        for nxt in store.neighbors(node):
            if nxt not in seen:seen.add(nxt);out.append(nxt);q.append((nxt,d+1))
    return out