class SegmentTree:

  '''Make a new Segment Tree. / O(N)'''
  def __init__(self, _n_or_a, op=lambda x,y: x+y, default=0) -> None:
    # assert 0 <= n <= 10**8
    self._op      = op
    self._default = default
    if type(_n_or_a) == int:
      self._n = _n_or_a
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._dat  = [self._default] * (self._size<<1)
    elif type(_n_or_a) == list:
      self._n = len(_n_or_a)
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._dat  = [self._default] * (self._size<<1)
      for i in range(self._n):
        self._dat[self._size+i] = _n_or_a[i]
      for i in range(self._size-1, 0, -1):
        self._dat[i] = self._op(self._dat[i<<1], self._dat[i<<1|1])
    else:
      raise TypeError

  '''Change a[p] into x. / O(logN)'''
  def set(self, indx: int, key) -> None:
    assert 0 <= indx <= self._n, f'indx={indx}, _n={self._n} <- must be 0 <= indx <= self._n'
    indx += self._size
    self._dat[indx] = key
    for i in range(self._log):
      indx >>= 1
      self._dat[indx] = self._op(self._dat[indx<<1], self._dat[indx<<1|1])

  '''Return a[indx]. / O(1)'''
  def get(self, indx: int):
    assert 0 <= indx and indx < self._n, f'indx={indx}, _n={self._n} <- must be 0 <= indx <= self._n'
    return self._dat[indx+self._size]

  def __getitem__(self, indx: int):
    return self.get(indx)

  def __setitem__(self, indx: int, key):
    self.set(indx, key)

  '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n, f'l={l},r={r} <- must be 0 <= l <= r <= self._n'
    l += self._size
    r += self._size
    lres, rres = self._default, self._default
    while l < r:
      if l & 1:
        lres = self._op(lres, self._dat[l])
        l += 1
      if r & 1:
        r ^= 1
        rres = self._op(self._dat[r], rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  '''Return op([0, n)). / O(1)'''
  def all_prod(self):
    return self._dat[1]

  '''Find the largest index R: f([l, R)) == True. / O(logN)'''
  def max_right(self, l: int, f=lambda lr: lr):
    # f(seg.prod(l, r)) == True 区間[l, r)が満たして欲しい条件
    assert 0 <= l <= self._n
    assert f(self._default)
    if l == self._n:
      return self._n 
    l += self._size
    tmp = self._default
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(tmp, self._dat[l])):
        while l < self._size:
          l <<= 1
          if f(self._op(tmp, self._dat[l])):
            tmp = self._op(tmp, self._dat[l])
            l |= 1
        return l - self._size
      tmp = self._op(tmp, self._dat[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  '''Find the smallest index L: f([L, r)) == True. / O(logN)'''
  def min_left(self, r: int, f=lambda lr: lr):
    assert 0 <= r <= self._n 
    assert f(self._default)
    if r == 0:
      return 0 
    r += self._size
    tmp = self._default
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._dat[r], tmp)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._dat[r], tmp)):
            tmp = self._op(self.dat[r], tmp)
            r ^= 1
        return r + 1 - self._size
      tmp = self._op(self._dat[r], tmp)
      if r & -r == r:
        break 
    return 0

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self._n)])) + ']'

  def show(self):
    ret = []
    for i in range(self._log+1):
      tmp = [' ']
      for j in range(2**i):
        tmp.append(self._dat[2**i+j])
      ret.append(' '.join(map(str, tmp)))
    print('<SegmentTree> [\n' + '\n'.join(map(str, ret)) + '\n]')



