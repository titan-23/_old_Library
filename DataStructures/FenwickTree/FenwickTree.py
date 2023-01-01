from typing import List, Union


class FenwickTree:

  '''Build a new FenwickTree. / O(N)'''
  def __init__(self, _n_or_a: Union[List[int], int]):
    if isinstance(_n_or_a, int):
      self._size = _n_or_a
      self._tree = [0] * (self._size+1)
    else:
      a = list(_n_or_a)
      self._size = len(a)
      self._tree = [0] + a
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          self._tree[i + (i & -i)] += self._tree[i]
    self._s = 1 << (self._size-1).bit_length()

  '''Return sum([0, r)) of a. / O(logN)'''
  def pref(self, r: int) -> int:
    assert r <= self._size
    ret = 0
    while r > 0:
      ret += self._tree[r]
      r -= r & -r
    return ret

  '''Return sum([l, n)) of a. / O(logN)'''
  def suff(self, l: int) -> int:
    assert 0 <= l < self._size
    return self.pref(self._size) - self.pref(l)

  '''Return sum([l, r)] of a. / O(logN)'''
  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self._size
    return self.pref(r) - self.pref(l)

  def __getitem__(self, k: int) -> int:
    return self.sum(k, k+1)

  '''Add x to a[k]. / O(logN)'''
  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self._size
    k += 1
    while k <= self._size:
      self._tree[k] += x
      k += k & -k

  '''bisect_left(acc)'''
  def bisect_left(self, w: int) -> int:
    i = 0
    s = self._s
    while s:
      if i + s <= self._size and self._tree[i + s] < w:
        w -= self._tree[i + s]
        i += s
      s >>= 1
    return i if w else None

  '''bisect_right(acc)'''
  def bisect_right(self, w: int) -> int:
    i = 0
    s = self._s
    while s:
      if i + s <= self._size and self._tree[i + s] <= w:
        w -= self._tree[i + s]
        i += s
      s >>= 1
    return i

  def show(self) -> None:
    print('[' + ', '.join(map(str, (self.pref(i) for i in range(self._size+1)))) + ']')

  def to_l(self) -> List[int]:
    return [self.__getitem__(i) for i in range(self._size)]

  @classmethod
  def inversion_num(self, a: List[int], compress: bool=False) -> int:
    ans = len(a)
    if compress:
      a_ = sorted(set(a))
      z = {e: i for i, e in enumerate(a_)}
      fw = FenwickTree(len(a_))
      for i, e in enumerate(a):
        fw.add(z[e], 1)
        ans += i - fw.pref(z[e])
    else:
      fw = FenwickTree(ans)
      for i, e in enumerate(a):
        fw.add(e, 1)
        ans += i - fw.pref(e)
    return ans

  def __str__(self):
    sub = [self.pref(i) for i in range(self._size+1)]
    return '[' + ', '.join(map(str, (sub[i+1]-sub[i] for i in range(self._size)))) + ']'

  def __repr__(self):
    return 'FenwickTree' + str(self)


