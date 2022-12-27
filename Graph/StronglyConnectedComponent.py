import sys


class SCC:

  def __init__(self, G: list):
    self._n = len(G)
    self._start, self._elist = self._csr(G)
    if sys.getrecursionlimit() < self._n+1:
      sys.setrecursionlimit(self._n+1)

  def _csr(self, G):
    start = [0] * (self._n + 1)
    E = []
    for v in range(self._n):
      for x in G[v]:
        E.append((v, x))
    elist = [0] * len(E)
    for e0,e1 in E:
      start[e0+1] += 1
    for i in range(1, self._n+1):
      start[i] += start[i-1]

    cnt = start[:]
    for e0, e1 in E:
      elist[cnt[e0]] = e1
      cnt[e0] += 1
    return start, elist

  def _scc_ids(self):

    now_ord = 0
    group_num = 0

    visited = []

    low = [0] * self._n
    ord_ = [-1] * self._n
    ids = [0] * self._n

    def _dfs(v):
      nonlocal now_ord, group_num, visited, low, ord_, ids

      low[v] = ord_[v] = now_ord
      now_ord += 1
      visited.append(v)

      for i in range(self._start[v], self._start[v+1]):
        to = self._elist[i]

        if ord_[to] == -1:
          _dfs(to)

          low[v] = min(low[v], low[to])
        else:
          low[v] = min(low[v], ord_[to])

      if low[v] == ord_[v]:
        while True:
          u = visited.pop()
          ord_[u] = self._n
          ids[u] = group_num
          if u == v:
            break
        group_num += 1


    for i in range(self._n):
      if ord_[i] == -1:
        _dfs(i)

    for i in range(self._n):
      ids[i] = group_num - 1 - ids[i]

    return group_num, ids

  def get_scc(self):
    group_num, ids = self._scc_ids()
    groups = [[] for _ in range(group_num)]
    for i in range(self._n):
      groups[ids[i]].append(i)
    return groups

  # 閉路検出：len(scc) == nかどうか
