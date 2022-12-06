# https://github.com/titanium-22/Library/blob/main/FenwickTree.py


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
    self._s = 1 << self._size.bit_length()

  '''Return sum([0, r)) of a. / O(logN)'''
  def pref(self, r: int) -> int:
    assert r <= self._size
    r += 1
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
    return self.pref(r - 1) - self.pref(l - 1)

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
    print('[' + ', '.join(map(str, [self.pref(i) for i in range(self._size)])) + ']')

  @classmethod
  def inversion_num(self, a: List[int], compress=False) -> int:
    ans = len(a)
    if compress or max(a) >= ans:
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
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self._size)])) + ']'

  def __repr__(self):
    return 'FenwickTree ' + str(self)


class FenwickTree2D:
 
  '''Build a new FenwickTree2D.'''
  def __init__(self, h: int, w: int, a: List[List[int]]=[]):
    self._h = h + 1
    self._w = w + 1
    self._bit = [[0]*(self._w) for _ in range(self._h)]
    if a:
      self._build(a)

  def _build(self, a):
    for i in range(self._h-1):
      for j in range(self._w-1):
        self.add(i, j, a[i][j])
 
  '''Add x to a[h][w]. / O(logH * logW)'''
  def add(self, h: int, w: int, x) -> None:
    h += 1
    w += 1
    while h < self._h:
      j = w
      while j < self._w:
        self._bit[h][j] += x
        j += j & -j
      h += h & -h
 
  '''Return sum([0, h) * [0, w)) of a. / O(logH * logW)'''
  def _sum(self, h: int, w: int):
    ret = 0
    while h > 0:
      j = w
      while j > 0:
        ret += self._bit[h][j]
        j -= j & -j
      h -= h & -h
    return ret
 
  '''Retrun sum([h1, h2) * [w1, w2)) of a. / O(logH * logW)'''
  def sum(self, h1: int, w1: int, h2: int, w2: int):
    assert h1 <= h2 and w1 <= w2
    # w1, w2 = min(w1, w2), max(w1, w2)
    # h1, h2 = min(h1, h2), max(h1, h2)
    return self._sum(h2, w2) - self._sum(h2, w1) - self._sum(h1, w2) + self._sum(h1, w1)

  def __str__(self):
    ret = []
    for i in range(self._h-1):
      tmp = []
      for j in range(self._w-1):
        tmp.append(self.sum(i, j, i+1, j+1))
      ret.append(', '.join(map(str, tmp)))
    return '[ ' + '\n  '.join(map(str, ret)) + ' ]'


class FenwickTreeRangeAdd:

  '''Build a new FenwickTreeRangeAdd.'''
  def __init__(self, n: int):
    self._n = n
    self.bit0 = FenwickTree(n+1)
    self.bit1 = FenwickTree(n+1)

  '''Add x to a[p]. / O(logN)'''
  def add(self, k: int, x: int) -> None:
    self.bit0.add(k, x)

  '''Add x to range( [l, r) ). / O(logN)'''
  def add_range(self, l: int, r: int, x: int) -> None:
    self.bit0.add(l, -x*l)
    self.bit0.add(r, x*r)
    self.bit1.add(l, x)
    self.bit1.add(r, -x)

  '''Return sum [l, r). / O(logN)'''
  def sum(self, l: int, r: int) -> int:
    return self.bit0.pref(r) + r*self.bit1.pref(r) - self.bit0.pref(l) - l*self.bit1.pref(l)

  def __getitem__(self, k: int):
    return self.sum(k, k+1)

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self._n)])) + ']'
