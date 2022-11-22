# https://github.com/titanium-22/Library/blob/main/UnionFind.py


from collections import defaultdict


class UnionFind:

  '''Build a new UnionFind. / O(N)'''
  def __init__(self, n: int):
    self.__n = n
    self.__group_numbers = n
    self.__parents = [-1] * n
    self.__G = [[] for _ in range(n)]

  def __find(self, x: int) -> int:
    a = x
    while self.__parents[a] >= 0:
      a = self.__parents[a]
    while self.__parents[x] >= 0:
      y = x
      x = self.__parents[x]
      self.__parents[y] = a
    return a

  '''Untie x and y. / O(α(N))'''
  def unite(self, x: int, y: int) -> None:
    x, y = self.__find(x), self.__find(y)
    if x == y:
      return
    self.__G[x].append(y)
    self.__G[y].append(x)
    self.__group_numbers -= 1
    if self.__parents[x] > self.__parents[y]:
      x, y = y, x
    self.__parents[x] += self.__parents[y]
    self.__parents[y] = x

  '''Return xが属する集合の要素数. / O(α(N))'''
  def size(self, x: int) -> int:
    return -self.__parents[self.__find(x)]

  '''Return True if 'same' else False. / O(α(N))'''
  def same(self, x: int, y: int) -> bool:
    return self.__find(x) == self.__find(y)

  '''Return set(the members of x). / O(size(x))'''
  def members(self, x: int) -> set:
    seen = set([x])
    todo = [x]
    while todo:
      v = todo.pop()
      for vv in self.__G[v]:
        if vv in seen:
          continue
        todo.append(vv)
        seen.add(vv)
    return seen

  '''Return all roots. / O(N)'''
  def roots(self) -> list:
    return [i for i, x in enumerate(self.__parents) if x < 0]

  '''Return the number of groups. / O(1)'''
  def group_count(self) -> int:
    return self.__group_numbers

  '''Return all_group_members. / O(Nα(N))'''
  def all_group_members(self) -> list:
    group_members = defaultdict(list)
    for member in range(self.__n):
      group_members[self.__find(member)].append(member)
    return group_members

  '''relax. / O(Nα(N))'''
  def relax(self) -> None:
    for i in range(self.__n):
      self.__find(i)

  '''Clear. / O(N)'''
  def clear(self) -> None:
    self.__group_numbers = self.__n
    self.__parents = [-1] * self.__n
    self.__G = [[] for _ in range(self.__n)]

  def __str__(self) -> str:
    ret = '<UnionFind> [\n'
    ret += '\n'.join(f' {k}: {v}' for k, v in self.all_group_members().items())
    ret += '\n]'
    return ret
