# https://github.com/titanium-22/Library/tree/main/Graph/dijkstra.py


from typing import List, Tuple
from heapq import heappush, heappop
inf = float('inf')

def dijkstra(G: List[List[int]], s: int) -> List[int]:
  dist = [inf] * len(G)
  dist[s] = 0
  hq = [(0, s)]
  while hq:
    d, v = heappop(hq)
    if dist[v] < d: continue
    for x, c in G[v]:
      if dist[x] > d + c:
        dist[x] = d + c
        heappush(hq, (d + c, x))
  return dist

'''Return (path: from s to t, dist: from s)'''
def dijkstra_path(G: List[List[int]], s: int, t: int) -> Tuple[List[int], List[int]]:
  prev = [-1] * len(G)
  dist = [inf] * len(G)
  dist[s] = 0
  hq = [(0, s)]
  while hq:
    d, v = heappop(hq)
    if dist[v] < d: continue
    for x, c in G[v]:
      if dist[x] > d + c:
        dist[x] = d + c
        prev[x] = v
        heappush(hq, (d + c, x))
  if dist[t] == inf:
    return [], dist
  path = []
  d = dist[t]
  while prev[t] != -1:
    path.append(t)
    t = prev[t]
  path.append(t)
  return path[::-1], dist
