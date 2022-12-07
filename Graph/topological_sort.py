# https://github.com/titanium-22/Library/blob/main/Graph/topological_sort.py


from typing import List
from heapq import heapify, heappush, heappop
from collections import deque
# len(toposo) != n: 閉路が存在

def topological_sort_min(G: List[List[int]]) -> List[int]:
  n = len(G)
  d = [0] * n
  for i in range(n):
    for x in G[i]:
      d[x] += 1
  hq = [i for i,a in enumerate(d) if not a]
  heapify(hq)
  ret = []
  while hq:
    v = heappop(hq)
    ret.append(v)
    for x in G[v]:
      d[x] -= 1
      if d[x] == 0:
        heappush(hq, x)
  return ret


def topological_sort(G: List[List[int]]) -> List[int]:
  "Return topological_sort. / O(|V|+|E|)"
  n = len(G)
  d = [0] * n
  outs = [[] for _ in range(n)]
  for v in range(n):
    for x in G[v]:
      d[x] += 1
      outs[v].append(x)
  res = []
  todo = deque([i for i in range(n) if d[i] == 0])
  while todo:
    v = todo.popleft()
    res.append(v)
    for x in outs[v]:
      d[x] -= 1
      if d[x] == 0:
        todo.append(x)
  return res

