class RootedTree:

  def __init__(self, _G: list, _root: int, lp=False, lca=False):
    self._n = len(_G)
    self._G = _G
    self._root = _root
    self._height = -1
    self._toposo = []
    self._dist = []
    self._descendant_num = []
    self._leaf = []
    self._leaf_num = []
    self._parents = []
    self._diameter = [-1, -1, -1]
    self._bipartite_graph = []
    self._lp = lp
    self._lca = lca
    self._rank = []
    K = 1
    while 1 << K < self._n:
      K += 1
    self._K = K
    self._doubling = [[-1]*self._n for _ in range(self._K)]
    self._calc_dist_toposo()
    if lp:
      self._calc_leaf_parents()
    if lca:
      self._calc_doubling()

  '''Return the number of vertex of self. / O(1)'''
  def __len__(self) -> int:
    return self._n

  def __str__(self) -> str:
    self._calc_leaf_parents()
    ret = ["<RootedTree> ["]
    ret.extend(
      [f'  dist:{str(d).zfill(2)} - v:{str(i).zfill(2)} - p:{str(self._parents[i]).zfill(2)} - child:{sorted(self._leaf[i])}'
       for i,d in sorted(enumerate(self._dist), key=lambda x: x[1])]
      )
    ret.append(']')
    return '\n'.join(ret)

  def _calc_dist_toposo(self) -> None:
    '''Calc dist and toposo. / O(N)'''
    todo = [self._root]
    self._dist = [-1] * self._n
    self._rank = [-1] * self._n
    self._dist[self._root] = 0
    self._rank[self._root] = 0
    self._toposo = [self._root]

    while todo:
      v = todo.pop()
      d = self._dist[v]
      r = self._rank[v]
      for x,c in self._G[v]:
        if self._dist[x] != -1:
          continue
        self._dist[x] = d + c
        self._rank[x] = r + 1
        todo.append(x)
        self._toposo.append(x)
    return

  def _calc_leaf_parents(self) -> None:
    '''Calc child and parents. / O(N)'''
    if self._leaf and self._leaf_num and self._parents:
      return
    self._leaf_num = [0] * self._n
    self._leaf = [[] for _ in range(self._n)]
    self._parents = [-1] * self._n

    for v in self._toposo[::-1]:
      for x,_ in self._G[v]:
        if self._rank[x] < self._rank[v]:
          self._parents[v] = x
          continue
        self._leaf[v].append(x)
        self._leaf_num[v] += 1
    return

  '''Return dist. / O(N)'''
  def get_dists(self) -> list:
    return self._dist

  '''Return toposo. / O(N)'''
  def get_toposo(self) -> list:
    return self._toposo

  '''Return height. / O(N)'''
  def get_height(self) -> int:
    if self._height > -1:
      return self._height
    self._height = max(self._dist)
    return self._height

  '''Return descendant_num. / O(N)'''
  def get_descendant_num(self) -> list:
    if self._descendant_num:
      return self._descendant_num
    self._descendant_num = [1] * self._n

    for v in self._toposo[::-1]:
      for x,c in self._G[v]:
        if self._dist[x] < self._dist[v]:
          continue
        self._descendant_num[v] += self._descendant_num[x]

    for i in range(self._n):
      self._descendant_num[i] -= 1
    return self._descendant_num

  '''Return child / O(N)'''
  def get_leaf(self) -> list:
    if self._leaf:
      return self._leaf
    self._calc_leaf_parents()
    return self._leaf

  '''Return child_num. / O(N)'''
  def get_leaf_num(self) -> list:
    if self._leaf_num:
      return self._leaf_num
    self._calc_leaf_parents()
    return self._leaf_num

  '''Return parents. / O(N)'''
  def get_parents(self) -> list:
    if self._parents:
      return self._parents
    self._calc_leaf_parents()
    return self._parents

  '''Return diameter of tree. / O(N)'''
  def get_diameter(self) -> int:
    if self._diameter[0] > -1:
      return self._diameter
    s = self._dist.index(self.get_height())
    todo = [s]
    ndist = [-1] * self._n
    ndist[s] = 0
    while todo:
      v = todo.pop()
      d = ndist[v]
      for x, c in self._G[v]:
        if ndist[x] != -1:
          continue
        ndist[x] = d + c
        todo.append(x)
    diameter = max(ndist)
    t = ndist.index(diameter)
    self._diameter = [diameter, s, t]
    return self._diameter

  '''Return [1 if root else 0]. / O(N)'''
  def get_bipartite_graph(self) -> list:
    if self._bipartite_graph:
      return self._bipartite_graph
    self._bipartite_graph = [-1] * self._n
    self._bipartite_graph[self._root] = 1
    todo = [self._root]
    while todo:
      v = todo.pop()
      nc = 0 if self._bipartite_graph[v] else 1
      for x,_ in self._G[v]:
        if self._bipartite_graph[x] != -1:
          continue
        self._bipartite_graph[x] = nc
        todo.append(x)
    return self._bipartite_graph

  def _calc_doubling(self) -> None:
    "Calc doubling if self._lca. / O(NlogN)"
    if not self._parents:
      self._calc_leaf_parents()
    for i in range(self._n):
      self._doubling[0][i] = self._parents[i]

    for k in range(self._K-1):
      for v in range(self._n):
        if self._doubling[k][v] < 0:
          self._doubling[k+1][v] = -1
        else:
          self._doubling[k+1][v] = self._doubling[k][self._doubling[k][v]]
    return

  '''Return LCA of (u, v). / O(logN)'''
  def get_lca(self, u: int, v: int) -> int:
    assert self._lca
    if self._rank[u] < self._rank[v]:
      u, v = v, u
    for k in range(self._K):
      if ((self._rank[u] - self._rank[v]) >> k) & 1:
        u = self._doubling[k][u]

    if u == v:
      return u
    for k in range(self._K-1, -1, -1):
      if self._doubling[k][u] != self._doubling[k][v]:
        u = self._doubling[k][u]
        v = self._doubling[k][v]
    return self._doubling[0][u]

  '''Return dist(u -- v). / O(logN)'''
  def get_dist(self, u: int, v: int) -> int:
    assert self._lca
    return self._dist[u] + self._dist[v] - 2*self._dist[self.get_lca(u, v)] + 1

  '''Return True if (a is on path(u - v)) else False. / O(logN)'''
  def is_on_path(self, u: int, v: int, a: int) -> bool:
    assert self._lca
    return self.get_dist(u, a) + self.get_dist(a, v) == self.get_dist(u, v)  # rank??

  '''Return path (u -> v).'''
  def get_path(self, u, v) -> list:
    assert self._lca
    if u == v: return [u]
    self.get_parents()
    def get_path_lca(u, v):
      path = []
      while u != v:
        u = self._parents[u]
        if u == v:
          break
        path.append(u)
      return path

    lca = self.get_lca(u, v)
    path = [u]
    path.extend(get_path_lca(u, lca))
    if u != lca and v != lca:
      path.append(lca)
    path.extend(get_path_lca(v, lca)[::-1])
    path.append(v)
    return path

  def dfs_in_out(self) -> list:
    curtime = -1
    todo = [~self._root, self._root]
    intime = [-1] * self._n
    outtime = [-1] * self._n
    seen = [False] * self._n
    seen[self._root] = True
    while todo:
      curtime += 1
      v = todo.pop()
      if v >= 0:
        intime[v] = curtime
        for x,_ in self._G[v]:
          if not seen[x]:
            todo.append(~x)
            todo.append(x)
            seen[x] = True
      else:
        outtime[~v] = curtime
    return intime, outtime



class EulerTour(RootedTree):
  "Need Class-RootedTree and Class-FenwickTree."

  def __init__(self, G: list, root: int, vertexcost=[], cp=False, lca=False) -> None:
    super().__init__(G, root, cp, lca)

    if not vertexcost:
      vertexcost = [0]*self._n

    path = []
    pathdepth = []

    vcost1 = []
    vcost2 = []
    ecost1 = []
    ecost2 = []

    nodein = [-1] * self._n
    nodeout = [-1] * self._n

    curtime = -1

    depth = [-1] * self._n
    depth[self._root] = 0

    todo = [(self._root, 0, 0, vertexcost[self._root])]
    while todo:
      curtime += 1
      cn, cd, vc, ec = todo.pop()
      if cn >= 0:  # 行きがけ
        if nodein[cn] == -1:
          nodein[cn] = curtime
        depth[cn] = cd
        pathdepth.append(cd)
        path.append(cn)

        ecost1.append(vc)
        ecost2.append(vc)
        vcost1.append(ec)
        vcost2.append(ec)
        if len(G[cn]) == 1:
          nodeout[cn] = curtime + 1
        for nn, nv in self._G[cn][::-1]:
          if depth[nn] != -1:
            continue
          todo.append((~cn, cd, nv, -vertexcost[nn]))
          todo.append((nn, cd+1, nv, vertexcost[nn]))
      else:
        cn = ~cn
        if nodein[cn] == -1:
          nodein[cn] = curtime
        path.append(cn)
        ecost1.append(0)
        ecost2.append(-vc)
        vcost1.append(0)
        vcost2.append(ec)
        pathdepth.append(cd)
        nodeout[cn] = curtime + 1

    path.append(-1)
    pathdepth.append(-1)
    vcost1.append(0)
    vcost2.append(-vertexcost[self._root])
    ecost1.append(0)
    ecost2.append(0)

    # ---------------------- #

    self._nodein = nodein
    self._nodeout = nodeout
    self._vertexcost = vertexcost
    self._path = path
    self._vertexcost = vertexcost
    
    self._vcost1 = FenwickTree(len(vcost1)+1)
    self._vcost2 = FenwickTree(len(vcost2)+1)
    self._ecost1 = FenwickTree(len(ecost1)+1)
    self._ecost2 = FenwickTree(len(ecost2)+1)

    self._pathdepth = []

    V = [(pd, i) for i,pd in enumerate(pathdepth)]
    # self._pathdepth = SegmentTree(len(pathdepth), op=lambda x,y:min(x,y), default=(inf, inf), V=V)

    # ---------------------- #


    for i,vc1 in enumerate(vcost1):
      self._vcost1.add(i, vc1)
    for i,vc2 in enumerate(vcost2):
      self._vcost2.add(i, vc2)
    for i,ec1 in enumerate(ecost1):
      self._ecost1.add(i, ec1)
    for i,ec2 in enumerate(ecost2):
      self._ecost2.add(i, ec2)

    return

  def get_lca_(self, x, y):
    l = min(self._nodein[x], self._nodein[y])
    r = max(self._nodeout[x], self._nodeout[y])
    ind = self._pathdepth.prod(l, r)
    return self._path[ind[1]]

  def lca_mul(self, L: list):
    l, r = inf, -inf
    for li in L:
      l = min(l, self._nodein[li])
      r = max(r, self._nodeout[li])
    ind = self._pathdepth.prod(l, r)
    return self._path[ind]

  def get_subtree_vcost(self, x):
    l = self._nodein[x]
    r = self._nodeout[x]
    return self._vcost1.sum(l, r)

  def get_subtree_ecost(self, x):
    l = self._nodein[x]
    r = self._nodeout[x]
    return self._ecost1.sum(l+1, r)

  def get_path_vcost1(self, x):
    # 頂点xを含む
    # Fenic_TreeとSegmentTreeは[l, r)なので、return文は右端に１を足している。
    return self._vcost2.sum(0, self._nodein[x]+1)

  def get_path_ecost1(self, x):
    # 根から頂点xまでの辺
    return self._ecost2.sum(0, self._nodein[x]+1)

  def get_path_vcost2(self, x, y):
    a = self.get_lca(x, y)
    return self.get_path_vcost1(x) + self.get_path_vcost1(y) - 2 * self.get_path_vcost1(a) + self._vertexcost[a]

  def get_path_ecost2(self, x, y):
    a = self.get_lca(x, y)
    return self.get_path_ecost1(x) + self.get_path_ecost1(y) - 2 * self.get_path_ecost1(a)

  def add_vertex(self, x: int, w: int) -> None:
    "Add w to vertex x. / O(logN)"
    l = self._nodein[x]
    r = self._nodeout[x]
    self._vcost1.add(l, w)
    # self._vcost1.add(r+1, -w)
    self._vcost2.add(l, w)
    self._vcost2.add(r+1, -w)
    self._vertexcost[x] += w
    return

  def add_edge(self, u: int, v: int, w: int) -> None:
    "Add w to edge([u - v]). / O(logN)"
    if self._rank[u] < self._rank[v]:
      # 葉側を調べる
      u, v = v, u
    l = self._nodein[u]
    r = self._nodeout[u]
    self._ecost1.add(l, w)
    self._ecost1.add(r+1, -w)
    self._ecost2.add(l, w)
    self._ecost2.add(r+1, -w)
    return


class LCA:

  def __init__(self, _G, _root):
    self._G = _G
    self._root = _root
    self._n = len(_G)
    self._inf = self._n+1
    path = []
    pathdepth = []
    nodein = [-1] * self._n
    nodeout = [-1] * self._n
    curtime = -1
    depth = [-1] * self._n
    depth[self._root] = 0
    todo = [(self._root, 0)]
    while todo:
      curtime += 1
      cn, cd = todo.pop()
      if cn >= 0:
        if nodein[cn] == -1:
          nodein[cn] = curtime
        depth[cn] = cd
        pathdepth.append(cd)
        path.append(cn)
        if len(self._G[cn]) == 1:
          nodeout[cn] = curtime + 1
        for nn in self._G[cn]:
          if depth[nn] != -1:
            continue
          todo.append((~cn, cd))
          todo.append((nn, cd+1))
      else:
        cn = ~cn
        if nodein[cn] == -1:
          nodein[cn] = curtime
        path.append(cn)
        pathdepth.append(cd)
        nodeout[cn] = curtime + 1

    path.append(-1)
    pathdepth.append(-1)

    # ---------------------- #

    self._nodein = nodein
    self._nodeout = nodeout
    self._path = path

    V = [(pd, i) for i, pd in enumerate(pathdepth)]
    self._pathdepth = SegmentTreeRangeMinimumQuery(V, default=(self._inf, self._inf))
  
  def get_lca(self, x: int, y: int):
    l = min(self._nodein[x], self._nodein[y])
    r = max(self._nodeout[x], self._nodeout[y])
    ind = self._pathdepth.prod(l, r)
    return self._path[ind[1]]

  def lca_mul(self, L: list):
    l, r = self._inf, -self._inf
    for li in L:
      l = min(l, self._nodein[li])
      r = max(r, self._nodeout[li])
    ind = self._pathdepth.prod(l, r)
    return self._path[ind]


