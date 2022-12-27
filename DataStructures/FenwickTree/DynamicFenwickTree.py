class DynamicFenwickTree:
 
  def __init__(self, n: int):
    self._size = n+1
    self._tree = {}
    self._s = 1 << n.bit_length()
 
  def add(self, k: int, x: int) -> None:
    k += 1
    while k <= self._size:
      if k in self._tree:
        self._tree[k] += x
      else:
        self._tree[k] = x
      k += k & -k
 
  '''Return sum([0, r)) of a. / O(logN)'''
  def pref(self, r: int) -> int:
    r += 1
    ret = 0
    while r > 0:
      if r in self._tree:
        ret += self._tree[r]
      r -= r & -r
    return ret
 
  def sum(self, l, r):
    return self.pref(r-1) - self.pref(l-1)
 
  '''bisect_left(acc)'''
  def bisect_left(self, w: int) -> int:
    i = 0
    s = self._s
    while s > 0:
      if i+s <= self._size:
        if i+s in self._tree and self._tree[i+s] < w:
          w -= self._tree[i+s]
          i += s
        elif i+s not in self._tree and 0 < w:
          i += s
      s >>= 1
    return i if w else None
 
  '''bisect_right(acc)'''
  def bisect_right(self, w: int) -> int:
    i = 0
    s = self._s
    while s > 0:
      if i+s <= self._size:
        if i+s in self._tree and self._tree[i+s] <= w:
          w -= self._tree[i+s]
          i += s
        elif i+s not in self._tree and 0 <= w:
          i += s
      s >>= 1
    return i
 