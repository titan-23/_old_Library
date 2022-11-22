# https://github.com/titanium-22/Library/blob/main/UnionFind/UnionFind.py


from collections import defaultdict


class UnionFind:

  '''Build a new UnionFind. / O(N)'''
  def __init__(self, n: int):
    self._n = n
    self._group_numbers = n
    self._parents = [-1] * n
    self._G = [[] for _ in range(n)]

  def _find(self, x: int) -> int:
    a = x
    while self._parents[a] >= 0:
      a = self._parents[a]
    while self._parents[x] >= 0:
      y = x
      x = self._parents[x]
      self._parents[y] = a
    return a

  '''Untie x and y. / O(α(N))'''
  def unite(self, x: int, y: int) -> None:
    x, y = self._find(x), self._find(y)
    if x == y:
      return
    self._G[x].append(y)
    self._G[y].append(x)
    self._group_numbers -= 1
    if self._parents[x] > self._parents[y]:
      x, y = y, x
    self._parents[x] += self._parents[y]
    self._parents[y] = x

  '''Return xが属する集合の要素数. / O(α(N))'''
  def size(self, x: int) -> int:
    return -self._parents[self._find(x)]

  '''Return True if 'same' else False. / O(α(N))'''
  def same(self, x: int, y: int) -> bool:
    return self._find(x) == self._find(y)

  '''Return set(the members of x). / O(size(x))'''
  def members(self, x: int) -> set:
    seen = set([x])
    todo = [x]
    while todo:
      v = todo.pop()
      for vv in self._G[v]:
        if vv in seen:
          continue
        todo.append(vv)
        seen.add(vv)
    return seen

  '''Return all roots. / O(N)'''
  def roots(self) -> list:
    return [i for i, x in enumerate(self._parents) if x < 0]

  '''Return the number of groups. / O(1)'''
  def group_count(self) -> int:
    return self._group_numbers

  '''Return all_group_members. / O(Nα(N))'''
  def all_group_members(self) -> list:
    group_members = defaultdict(list)
    for member in range(self._n):
      group_members[self._find(member)].append(member)
    return group_members

  '''Compress path. / O(Nα(N))'''
  def compress_path(self) -> None:
    for i in range(self._n):
      self._find(i)

  '''Clear. / O(N)'''
  def clear(self) -> None:
    self._group_numbers = self._n
    self._parents = [-1] * self._n
    self._G = [[] for _ in range(self._n)]

  def __str__(self) -> str:
    ret = '<UnionFind> [\n'
    ret += '\n'.join(f' {k}: {v}' for k, v in self.all_group_members().items())
    ret += '\n]'
    return ret