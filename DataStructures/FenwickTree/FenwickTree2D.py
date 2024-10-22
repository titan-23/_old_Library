from typing import List

class FenwickTree2D():

  '''Build a new FenwickTree2D. / O(HW)'''
  def __init__(self, h: int, w: int, a: List[List[int]]=[]):
    self._h = h + 1
    self._w = w + 1
    self._bit = [[0]*(self._w) for _ in range(self._h)]
    if a:
      assert len(a) == h and len(a[0]) == w
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
      bit_h = self._bit[h]
      while j < self._w:
        bit_h[j] += x
        j += j & -j
      h += h & -h

  def set(self, h: int, w: int, x) -> None:
    self.add(h, w, x-self.get(h, w))

  '''Return sum([0, h) * [0, w)) of a. / O(logH * logW)'''
  def _sum(self, h: int, w: int):
    ret = 0
    while h > 0:
      j = w
      bit_h = self._bit[h]
      while j > 0:
        ret += bit_h[j]
        j -= j & -j
      h -= h & -h
    return ret

  '''Retrun sum([h1, h2) * [w1, w2)) of a. / O(logH * logW)'''
  def sum(self, h1: int, w1: int, h2: int, w2: int):
    assert h1 <= h2 and w1 <= w2
    # w1, w2 = min(w1, w2), max(w1, w2)
    # h1, h2 = min(h1, h2), max(h1, h2)
    return self._sum(h2, w2) - self._sum(h2, w1) - self._sum(h1, w2) + self._sum(h1, w1)

  def get(self, h: int, w: int):
    return self.sum(h, h+1, w, w+1)

  def __str__(self):
    ret = []
    for i in range(self._h-1):
      ret.append(', '.join(map(str, ((self.sum(i, j, i+1, j+1)) for j in range(self._w-1)))))
    return '[ ' + '\n  '.join(map(str, ret)) + ' ]'

