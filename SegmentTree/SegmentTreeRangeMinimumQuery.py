class SegmentTreeRangeMinimumQuery:

  '''Make a new Segment Tree. / O(N)'''
  def __init__(self, _n_or_l, default):
    # assert 0 <= n <= 10**8

    self._default = default

    if type(_n_or_l) == int:
      self._n = _n_or_l
      self._log     = (self._n-1).bit_length()
      self._size    = 1 << self._log
      self._dat     = [self._default] * (2*self._size)
    elif type(_n_or_l) == list:
      self._n = len(_n_or_l)
      self._log     = (self._n-1).bit_length()
      self._size    = 1 << self._log
      self._dat     = [self._default] * (2*self._size)
      for i in range(self._n):
        self._dat[self._size+i] = _n_or_l[i]
      for i in range(self._size-1, 0, -1):
        self._dat[i] = self._dat[i<<1] if self._dat[i<<1] < self._dat[i<<1|1] else self._dat[i<<1|1]
    else:
      raise TypeError

  def set(self, p: int, x):
    '''Change a[p] into x. / O(logN)'''
    assert 0 <= p <= self._n, f'p={p}, _n={self._n} <- must be 0 <= p <= self._n'
    p += self._size
    self._dat[p] = x
    for _ in range(self._log):
      p >>= 1
      self._dat[p] = self._dat[p<<1] if self._dat[p<<1] < self._dat[p<<1|1] else self._dat[p<<1|1]

  def get(self, p: int):
    '''Return a[p]. / O(1)'''
    assert 0 <= p < self._n, f'p={p}, _n={self._n} <- must be 0 <= p <= self._n'
    return self._dat[p+self._size]

  def __getitem__(self, p: int):
    return self.get(p)

  def __setitem__(self, p: int, key):
    self.set(p, key)

  def prod(self, l: int, r: int):
    '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
    assert 0 <= l <= r <= self._n, f'l={l},r={r} <- must be 0 <= l <= r <= self._n'
    l += self._size
    r += self._size
    res = self._default
    while l < r:
      if l & 1:
        if res > self._dat[l]:
          res = self._dat[l]
        l += 1
      if r & 1:
        r ^= 1
        if res > self._dat[r]:
          res = self._dat[r]
      l >>= 1
      r >>= 1
    return res

  def all_prod(self):
    '''Return op([0, n)). / O(1)'''
    return self._dat[1]

  def max_right(self, l: int, f=lambda lr: lr):
    '''Find the largest index R: f([l, R)) == True. / O(logN)'''
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
      if not f(min(tmp, self._dat[l])):
        while l < self._size:
          l <<= 1
          if f(min(tmp, self._dat[l])):
            tmp = min(tmp, self._dat[l])
            l += 1
        return l - self._size
      tmp = min(tmp, self._dat[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f=lambda lr: lr):
    '''Find the smallest index L: f([L, r)) == True. / O(logN)'''
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
      if not f(min(self._dat[r], tmp)):
        while r < self._size:
          r = 2*r + 1
          if f(min(self._dat[r], tmp)):
            tmp = min(self.dat[r], tmp)
            r -= 1
        return r + 1 - self._size
      tmp = min(self._dat[r], tmp)
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


