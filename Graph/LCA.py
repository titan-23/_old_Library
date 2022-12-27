from typing import List


class LCA:

  def __init__(self, _G: List[List[int]], _root: int=0):
    self._n = len(_G)
    bit = self._n.bit_length()+1
    self._msk = (1<<bit)-1
    path = [-1] * (2*self._n-1)
    depth = [-1] * (2*self._n-1)
    nodeid = [-1] * self._n
    todo = [(_root, -1<<bit)]
    nowt = -1
    while todo:
      v, pd = todo.pop()
      nowt += 1
      d = pd & self._msk
      if v >= 0:
        p = pd >> bit
        nodeid[v] = nowt
        path[nowt] = v
        depth[nowt] = d
        for x in _G[v]:
          if x != p:
            todo.append((~v, (p<<bit)+d))
            todo.append((x, (v<<bit)+d+1))
      else:
        path[nowt] = ~v
        depth[nowt] = d
    self._path = path
    self._nodeid = nodeid
    self._depth = depth
    self._st = SparseTableRMQ((d<<bit)+i for i, d in enumerate(depth))

  def lca(self, x: int, y: int):
    l = self._nodeid[x]
    r = self._nodeid[y]
    if l > r:
      l, r = r, l
    return self._path[self._st.prod(l, r+1)&self._msk]

  def lca_mul(self, a: list):
    l = self._n
    r = -l
    for e in a:
      e = self._nodeid[e]
      if l > e: l = e
      if r < e: r = e
    return self._path[self._st.prod(l, r+1)]

  def dist(self, x: int, y: int) -> int:
    # assert all costs are 1.
    lca = self.lca(x, y)
    return self._depth[self._nodeid[x]] + self._depth[self._nodeid[y]] - 2*self._depth[self._nodeid[lca]]


