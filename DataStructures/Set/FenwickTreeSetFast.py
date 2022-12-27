# 0以上n未満の整数を管理できます 速いです
from typing import Union, Tuple, List, Iterable
class FenwickTreeSetFast:

  class InternalFenwickTree:

    def __init__(self, _n_or_a: Union[int, List[int]]):
      if isinstance(_n_or_a, int):
        self._size = _n_or_a
        self._tree = [0] * (self._size+1)
      else:
        self._size = len(_n_or_a)
        self._tree = [0] + _n_or_a
        for i in range(1, self._size):
          if i + (i & -i) <= self._size:
            self._tree[i + (i & -i)] += self._tree[i]
      self._s = 1 << (self._size-1).bit_length()

    def pref(self, r: int) -> int:
      r += 1
      ret = 0
      while r > 0:
        ret += self._tree[r]
        r -= r & -r
      return ret

    def add(self, k: int, x: int) -> None:
      k += 1
      while k <= self._size:
        self._tree[k] += x
        k += k & -k

    def bisect_left(self, w: int) -> int:
      i = 0
      s = self._s
      while s > 0:
        if i + s <= self._size and self._tree[i + s] < w:
          w -= self._tree[i + s]
          i += s
        s >>= 1
      return i if w else None

    def bisect_right(self, w: int) -> int:
      i = 0
      s = self._s
      while s > 0:
        if i + s <= self._size and self._tree[i + s] <= w:
          w -= self._tree[i + s]
          i += s
        s >>= 1
      return i

  # Build a new FenwickTreeSetFast. / O(len(A) log(len(A)))
  def __init__(self, _n: int, a: Iterable[int]=[]):
    self._len = 0
    self._size = _n
    self._cnt = bytearray(_n)
    if a:
      a_ = [0] * _n
      for v in a:
        if a_[v] == 0:
          self._len += 1
          self._cnt[v] = 1
          a_[v] = 1
    self._fw = self.InternalFenwickTree(a_) if a else self.InternalFenwickTree(_n)

  def add(self, key: int) -> bool:
    if self._cnt[key] == 0:
      self._len += 1
      self._cnt[key] = 1
      self._fw.add(key, 1)
      return True
    return False

  def remove(self, key: int) -> None:
    if not self.discard(key):
      raise KeyError(key)

  def discard(self, key: int) -> bool:
    if self._cnt[key]:
      self._len -= 1
      self._cnt[key] = 0
      self._fw.add(key, -1)
      return True
    return False

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: int) -> Union[int, None]:
    if self._cnt[key]: return key
    pref = self._fw.pref(key - 1) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: int) -> Union[int, None]:
    pref = self._fw.pref(key - 1) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: int) -> Union[int, None]:
    if self._cnt[key]: return key
    pref = self._fw.pref(key)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: int) -> Union[int, None]:
    pref = self._fw.pref(key)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key: int) -> int:
    return self._fw.pref(key-1)

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key: int) -> int:
    return self._fw.pref(key)

  def pop(self, k: int=-1) -> int:
    if k < 0: k += self._len
    self._len -= 1
    i = 0
    s = self._fw._s
    while s > 0:
      if i+s <= self._size:
        if self._fw._tree[i+s] <= k:
          k -= self._fw._tree[i+s]
          i += s
        else:
          self._fw._tree[i+s] -= 1
      s >>= 1
    self._cnt[i] = 0
    return i

  def popleft(self) -> int:
    return self.pop(0)

  def __getitem__(self, k):
    if k < 0: k += self._len
    return self._fw.bisect_right(k)

  def __contains__(self, key: int):
    return self._cnt[key]

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter == self._len:
      raise StopIteration
    res = self.__getitem__(self._iter)
    self._iter += 1
    return res

  def __reversed__(self):
    for i in range(self._len):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return self._len

  def __bool__(self):
    return self._len > 0

  def __repr__(self):
    return 'FenwickTreeSetFast' + str(self)

