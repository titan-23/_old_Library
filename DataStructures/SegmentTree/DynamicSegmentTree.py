from typing import Generic, Iterable, TypeVar, Callable, Union, List, Dict
T = TypeVar('T')

class DynamicSegmentTree(Generic[T]):

  def __init__(self, u: int, a: Iterable[T]=[], _op: Callable[[T, T], T], _e: T) -> None:
    '''Build a new DynamicSegmentTree. / O(1)'''
    self._op = _op
    self._e = _e
    self._u = u
    self._log  = (self._u-1).bit_length()
    self._size = 1 << self._log
    self._data: Dict[int, T] = {}
    for i, a in enumerate(A):
      self.set(i, a)

  def set(self, k: int, val: T) -> None:
    '''Update a[k] <- x. / O(logU)'''
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.set({k}: int, {val}: T), n={self._u}'
    if k < 0: k += self._u
    k += self._size
    self._data[k] = val
    e = self._e
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._op(self._data.get(k<<1, e), self._data.get(k<<1|1, e))

  def get(self, k: int) -> T:
    '''Return a[k]. / O(1)'''
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.get({k}: int), n={self._u}'
    if k < 0: k += self._u
    return self._data.get(k+self._size, self.e)

  def prod(self, l: int, r: int) -> T:
    '''Return op([l, r)). / O(logU)'''
    assert 0 <= l <= r <= self._u, \
        f'IndexError: DynamicSegmentTree.prod({l}: int, {r}: int)'
    l += self._size
    r += self._size
    e = self._e
    lres = e
    rres = e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data.get(l, e))
        l += 1
      if r & 1:
        rres = self._op(self._data.get(r^1, e), rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self) -> T:
    '''Return op([0, n)). / O(1)'''
    return self._data[1]

  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    '''Find the largest index R s.t. f([l, R)) == True. / O(logU)'''
    assert 0 <= l <= self._u, \
        f'IndexError: DynamicSegmentTree.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'DynamicSegmentTree.max_right({l}, f), f({self._e}) must be true.'
    if l == self._u:
      return self._u 
    l += self._size
    e = self._e
    s = e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(s, self._data.get(l, e))):
        while l < self._size:
          l <<= 1
          if f(self._op(s, self._data.get(l, e))):
            s = self._op(s, self._data.get(l, e))
            l |= 1
        return l - self._size
      s = self._op(s, self._data.get(l, e))
      l += 1
      if l & -l == l:
        break
    return self._u

  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    '''Find the smallest index L s.t. f([L, r)) == True. / O(logU)'''
    assert 0 <= r <= self._u, \
        f'IndexError: DynamicSegmentTree.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'DynamicSegmentTree.min_left({r}, f), f({self._e}) must be true.'
    if r == 0:
      return 0 
    r += self._size
    e = self._e
    s = e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._data.get(r, e), s)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._data.get(r, e), s)):
            s = self._op(self._data.get(r, e), s)
            r ^= 1
        return r + 1 - self._size
      s = self._op(self._data.get(r, e), s)
      if r & -r == r:
        break 
    return 0

  def tolist(self) -> List[T]:
    '''Return List[self]. / O(NlogN)'''
    return [self.get(i) for i in range(self._u)]

  def __getitem__(self, k: int) -> T:
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.__getitem__({k}: int), n={self._u}'
    return self.get(k)

  def __setitem__(self, k: int, val: T) -> None:
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.__setitem__{k}: int, {val}: T), n={self._u}'
    self.set(k, val)

  def __str__(self) -> str:
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __repr__(self) -> str:
    return f'DynamicSegmentTree({self})'


def op(s, t):
  return
 
e = None

