from typing import List, Iterable, Union

class FenwickTreeRAQ():

  def __init__(self, _n_or_a: Union[Iterable[int], int]):
    if isinstance(_n_or_a, int):
      self.n = _n_or_a
      self.bit0 = [0] * (_n_or_a + 2)
      self.bit1 = [0] * (_n_or_a + 2)
      self.bit_size = self.n + 1
    else:
      if not hasattr(_n_or_a, '__len__'):
        _n_or_a = list(_n_or_a)
      self.n = len(_n_or_a)
      self.bit0 = [0] * (self.n + 2)
      self.bit1 = [0] * (self.n + 2)
      self.bit_size = self.n + 1
      for i, e in enumerate(_n_or_a):
        self.add_range(i, i+1, e)

  def __add(self, bit: List[int], k: int, x: int) -> None:
    k += 1
    while k <= self.bit_size:
      bit[k] += x
      k += k & -k

  def __pref(self, bit: List[int], r: int) -> int:
    ret = 0
    while r > 0:
      ret += bit[r]
      r -= r & -r
    return ret

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self.n, \
        f'IndexError: FenwickTreeRAQ.add({k}, {x}), n={self.n}'
    self.add_range(k, k+1, x)

  def add_range(self, l: int, r: int, x: int) -> None:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: FenwickTreeRAQ.add_range({l}, {r}, {x}), l={l},r={r},n={self.n}'
    self.__add(self.bit0, l, -x*l)
    self.__add(self.bit0, r, x*r)
    self.__add(self.bit1, l, x)
    self.__add(self.bit1, r, -x)

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: FenwickTreeRAQ.sum({l}, {r}), l={l},r={r},n={self.n}'
    return self.__pref(self.bit0, r) + r*self.__pref(self.bit1, r) - self.__pref(self.bit0, l) - l*self.__pref(self.bit1, l)

  def tolist(self) -> List[int]:
    return [self.sum(i, i+1) for i in range(self.n)]

  def __getitem__(self, k: int):
    assert 0 <= k < self.n, \
        f'IndexError: FenwickTreeRAQ.__getitem__({k}), n={self.n}'
    return self.sum(k, k+1)

  def __str__(self):
    return '[' + ', '.join(map(str, (self.sum(i, i+1) for i in range(self.n)))) + ']'

  def __repr__(self):
    return f'FenwickTreeRAQ({self})'

