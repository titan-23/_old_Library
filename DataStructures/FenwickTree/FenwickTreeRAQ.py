from typing import List, Iterable


class FenwickTreeRAQ:

  '''Build a new FenwickTreeRAQ.'''
  def __init__(self, n: int, a: Iterable[int]=[]):
    self._n = n
    self.bit0 = FenwickTree(n+1)
    self.bit1 = FenwickTree(n+1)
    for i, a_ in enumerate(a):
      self.add(i, a_)

  '''Add x to a[k]. / O(logN)'''
  def add(self, k: int, x: int) -> None:
    self.add_range(k, k+1, x)

  '''Add x to [l, r). / O(logN)'''
  def add_range(self, l: int, r: int, x: int) -> None:
    self.bit0.add(l, -x*l)
    self.bit0.add(r, x*r)
    self.bit1.add(l, x)
    self.bit1.add(r, -x)

  '''Return sum [l, r). / O(logN)'''
  def sum(self, l: int, r: int) -> int:
    return self.bit0.pref(r) + r*self.bit1.pref(r) - self.bit0.pref(l) - l*self.bit1.pref(l)

  def to_l(self) -> List[int]:
    return [self.sum(i, i+1) for i in range(self._n)]

  def __getitem__(self, k: int):
    return self.sum(k, k+1)

  def __str__(self):
    return '[' + ', '.join(map(str, (self.__getitem__(i) for i in range(self._n)))) + ']'

  def __repr__(self):
    return 'FenwickTreeRAQ' + str(self)


