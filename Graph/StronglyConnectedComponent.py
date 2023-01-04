from typing import List

'''Strongly Connected Components. / O(N+M)'''
# コンセプト：
# - 非再帰
# - グラフGは単純でなくてもよい
def get_scc(G: List[List[int]]) -> List[List[int]]:
  n = len(G)
  rG = [[] for _ in range(n)]
  for v in range(n):
    for x in G[v]:
      rG[x].append(v)
  visited = [0] * n
  toposo = [None] * n
  now = n
  for s in range(n):
    if visited[s]: continue
    todo = [~s, s]
    while todo:
      v = todo.pop()
      if v >= 0:
        if visited[v]: continue
        visited[v] = 2
        for x in G[v]:
          if visited[x]: continue
          todo.append(~x)
          todo.append(x)
      else:
        v = ~v
        if visited[v] == 1: continue
        visited[v] = 1
        now -= 1
        toposo[now] = v
  res = []
  for s in toposo:
    if not visited[s]: continue
    todo = [s]
    for v in todo:
      visited[v] = 0
      for x in rG[v]:
        if not visited[x]: continue
        visited[x] = 0
        todo.append(x)
    res.append(todo)
  return res

