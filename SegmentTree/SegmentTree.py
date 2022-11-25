# https://github.com/titanium-22/Library/blob/main/SegmentTree/SegmentTree.py


from typing import Generic, Iterable, TypeVar, Callable, Union
S = TypeVar("S")


class SegmentTree(Generic[S]):

  '''Build a new Segment Tree. / O(N)'''
  def __init__(self, _n_or_a: Union[int, Iterable[S]], _op: Callable[[S, S], S], _e: S) -> None:
    self._op = _op
    self._e = _e
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
        self._data[i] = self._op(self._data[i<<1], self._data[i<<1|1])

  '''Change a[p] into x. / O(logN)'''
  def set(self, key: int, val: S) -> None:
    assert 0 <= key < self._n
    key += self._size
    self._data[key] = val
    for _ in range(self._log):
      key >>= 1
      self._data[key] = self._op(self._data[key<<1], self._data[key<<1|1])

  '''Return a[key]. / O(1)'''
  def get(self, key: int) -> S:
    assert 0 <= key < self._n
    return self._data[key+self._size]

  '''Return op([l, r)). / O(logN)'''
  def prod(self, l: int, r: int) -> S:
    assert 0 <= l <= r <= self._n
    l += self._size
    r += self._size
    lres, rres = self._e, self._e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data[l])
        l += 1
      if r & 1:
        r ^= 1
        rres = self._op(self._data[r], rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  '''Return op([0, n)). / O(1)'''
  def all_prod(self) -> S:
    return self._data[1]

  '''Find the largest index R s.t. f([l, R)) == True. / O(logN)'''
  def max_right(self, l: int, f: Callable[[S], bool]) -> int:
    # f(seg.prod(l, r)) == True 区間[l, r)が満たして欲しい条件
    assert 0 <= l <= self._n
    assert f(self._e)
    if l == self._n:
      return self._n 
    l += self._size
    tmp = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(tmp, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(self._op(tmp, self._data[l])):
            tmp = self._op(tmp, self._data[l])
            l |= 1
        return l - self._size
      tmp = self._op(tmp, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  '''Find the smallest index L s.t. f([L, r)) == True. / O(logN)'''
  def min_left(self, r: int, f: Callable[[S], bool]) -> int:
    assert 0 <= r <= self._n 
    assert f(self._e)
    if r == 0:
      return 0 
    r += self._size
    tmp = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._data[r], tmp)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._data[r], tmp)):
            tmp = self._op(self._data[r], tmp)
            r ^= 1
        return r + 1 - self._size
      tmp = self._op(self._data[r], tmp)
      if r & -r == r:
        break 
    return 0

  def __getitem__(self, key: int) -> S:
    return self.get(key)

  def __setitem__(self, key: int, val: S) -> None:
    self.set(key, val)

  def __str__(self):
    return '[' + ', '.join(map(str, [self.get(i) for i in range(self._n)])) + ']'

  def show(self):
    ret = ['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]
    print('<SegmentTree> [\n' + '\n'.join(ret) + '\n]')


def op(s: S, t: S) -> S:
  return

e: S = None

