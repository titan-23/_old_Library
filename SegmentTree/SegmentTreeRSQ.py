# https://github.com/titanium-22/Library/blob/main/SegmentTree/SegmentTreeRSQ.py


from typing import Generic, Iterable, TypeVar, Callable, Union
T = TypeVar("T")


# RangeSumQuery.
class SegmentTreeRSQ(Generic[T]):

  '''Build a new SegmentTree. / O(N)'''
  def __init__(self, _n_or_a: Union[int, Iterable[T]], e: T=0) -> None:
    self._e = e
    if isinstance(_n_or_a, int):
      self._n = _n_or_a
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data  = [self._e] * (self._size<<1)
    else:
      _n_or_a = list(_n_or_a)
      self._n = len(_n_or_a)
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size<<1)
      self._data[self._size:self._size+self._n] = _n_or_a
      for i in range(self._size-1, 0, -1):
        self._data[i] = self._data[i<<1] + self._data[i<<1|1]

  '''Change a[k] into x. / O(logN)'''
  def set(self, k: int, key: T) -> None:
    assert 0 <= k < self._n
    k += self._size
    self._data[k] = key
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._data[k<<1] + self._data[k<<1|1]

  '''Return a[k]. / O(1)'''
  def get(self, k: int) -> T:
    assert 0 <= k < self._n
    return self._data[k+self._size]

  def __getitem__(self, k: int):
    return self.get(k)

  def __setitem__(self, k: int, key):
    self.set(k, key)

  '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n
    l += self._size
    r += self._size
    res = self._e
    while l < r:
      if l & 1:
        res += self._data[l]
        l += 1
      if r & 1:
        r ^= 1
        res += self._data[r]
      l >>= 1
      r >>= 1
    return res

  '''Return sum([0, n)). / O(1)'''
  def all_prod(self):
    return self._data[1]

  '''Find the largest index R: f([l, R)) == True. / O(logN)'''
  def max_right(self, l: int, f=lambda lr: lr):
    # f(seg.prod(l, r)) == True 区間[l, r)が満たして欲しい条件
    assert 0 <= l <= self._n
    assert f(0)
    if l == self._n:
      return self._n 
    l += self._size
    tmp = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(tmp + self._data[l]):
        while l < self._size:
          l <<= 1
          if f(tmp + self._data[l]):
            tmp += self._data[l]
            l += 1
        return l - self._size
      tmp += self._data[l]
      l += 1
      if l & -l == l:
        break
    return self._n

  '''Find the smallest index L: f([L, r)) == True. / O(logN)'''
  def min_left(self, r: int, f=lambda lr: lr):
    assert 0 <= r <= self._n 
    assert f(0)
    if r == 0:
      return 0 
    r += self._size
    tmp = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._data[r] + tmp):
        while r < self._size:
          r = r<<1|1
          if f(self._data[r] + tmp):
            tmp += self._data[r]
            r -= 1
        return r + 1 - self._size
      tmp += self._data[r]
      if r & -r == r:
        break 
    return 0

  def __str__(self):
    return '[' + ', '.join(map(str, [self.get(i) for i in range(self._n)])) + ']'

  def show(self):
    ret = []
    for i in range(self._log+1):
      tmp = [' ']
      for j in range(1<<i):
        tmp.append(self._data[1<<i+j])
      ret.append(' '.join(map(str, tmp)))
    print('<SegmentTreeRSQ> [\n' + '\n'.join(map(str, ret)) + '\n]')

