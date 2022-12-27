from typing import Generic, Iterable, TypeVar, Callable, Union
T = TypeVar("T")
F = TypeVar("F")


class LazySegmetTree(Generic[T, F]):
  
  def __init__(self, _n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[[F, F], F], e: T, id_: F) -> None:
    self._op = op
    self._mapping = mapping
    self._composition = composition
    self._e = e
    if isinstance(_n_or_a, int):
      self._n = _n_or_a
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size<<1)
    else:
      _n_or_a = list(_n_or_a)
      self._n = len(_n_or_a)
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size<<1)
      self._data[self._size:self._size+self._n] = _n_or_a
      for i in range(self._size - 1, 0, -1):
        self._data[i] = self._op(self._data[i << 1], self._data[i << 1 | 1])
    self._lazy = [id_] * (self._size)

  def _eval_at(self, i: int, f: F) -> None:
    self._data[i] = self._mapping(f, self._data[i])
    if i < self._size:
      self._lazy[i] = self._composition(f, self._lazy[i])

  def _propagate_above(self, i):
    H = i.bit_length() - 1
    for h in range(H, 0, -1):
        if self._lazy[i>>h] == 0:
          continue
        self._eval_at(i >> h << 1, self._lazy[i >> h])
        self._eval_at(i >> h << 1 | 1, self._lazy[i >> h])
        self._lazy[i >> h] = 0

  def __recalc_above(self, i):
    while i > 1:
      i >>= 1
      self._data[i] = self._op(self._data[i << 1], self._data[i << 1 | 1])

  def __setitem__(self, i, x):
    i += self._size
    self._propagate_above(i)
    self._data[i] = x
    self.__recalc_above(i)

  def __getitem__(self, i: int):
    i += self._size
    self._propagate_above(i)
    return self._data[i]

  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n
    if l == r:
      return self._e
    l += self._size
    r += self._size
    self._propagate_above(l // (l & -l))
    self._propagate_above(r // (r & -r) - 1)
    lres = self._e
    rres = self._e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data[l])
        l += 1
      if r & 1:
        r -= 1
        rres = self._op(self._data[r], rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self):
    return self._data[1]

  def apply(self, l, r, f):
    assert 0 <= l <= r <= self._n
    if l == r:
      return
    l += self._size
    r += self._size
    l0 = l // (l & -l)
    r0 = r // (r & -r) - 1
    self._propagate_above(l0)
    self._propagate_above(r0)
    while l < r:
      if l & 1:
        self._eval_at(l, f)
        l += 1
      if r & 1:
        r -= 1
        self._eval_at(r, f)
      l >>= 1
      r >>= 1
    self.__recalc_above(l0)
    self.__recalc_above(r0)


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None
id_ = None

