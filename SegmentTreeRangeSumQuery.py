class SegmentTreeRangeSumQuery:

  '''Make a new Segment Tree. / 0 <= n <= 10**8. / O(N)" # default=lambda x:0 '''
  def __init__(self, _n_or_a):
    if type(_n_or_a) == int:
      self._n = _n_or_a
      self._log     = (self._n-1).bit_length()
      self._size    = 1 << self._log
      self._dat     = [0] * (2*self._size)
    elif type(_n_or_a) == list:
      self._n = len(_n_or_a)
      self._log     = (self._n-1).bit_length()
      self._size    = 1 << self._log
      self._dat     = [0] * (2*self._size)
      for i in range(self._n):
        self._dat[self._size+i] = _n_or_a[i]
      for i in range(self._size-1, 0, -1):
        self._dat[i] = self._dat[2*i] + self._dat[2*i+1]
    else:
      raise TypeError

  '''Update a[p] into x. / O(logN)'''
  def set(self, p: int, x):
    assert 0 <= p <= self._n, f'p={p}, _n={self._n} <- must be 0 <= p <= self._n'
    p += self._size
    self._dat[p] = x
    for i in range(self._log):
      p >>= 1
      self._dat[p] = self._dat[p<<1] + self._dat[p<<1|1]

  '''Return a[p]. / O(1)'''
  def get(self, p: int):
    assert 0 <= p < self._n, f'p={p}, _n={self._n} <- must be 0 <= p <= self._n'
    return self._dat[p+self._size]

  def __getitem__(self, p: int):
    return self.get(p)

  def __setitem__(self, p: int, key):
    self.set(p, key)

  '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n, f'l={l},r={r} <- must be 0 <= l <= r <= self._n'
    l += self._size
    r += self._size
    res = 0
    while l < r:
      if l & 1:
        res += self._dat[l]
        l += 1
      if r & 1:
        r ^= 1
        res += self._dat[r]
      l, r = l>>1, r>>1
    return res

  '''Return sum([0, n)). / O(1)'''
  def all_prod(self):
    return self._dat[1]

  '''Find the largest index R: f([l, R)) == True. / O(logN)'''
  def max_right(self, l: int, f=lambda lr: lr):
    # f(seg.prod(l, r)) == True 区間[l, r)が満たして欲しい条件
    assert 0 <= l <= self._n
    assert f(0)
    if l == self._n:
      return self._n 
    l += self._size
    tmp = 0
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(tmp + self._dat[l]):
        while l < self._size:
          l <<= 1
          if f(tmp + self._dat[l]):
            tmp += self._dat[l]
            l += 1
        return l - self._size
      tmp += self._dat[l]
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
    tmp = 0
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._dat[r] + tmp):
        while r < self._size:
          r = r<<1|1
          if f(self._dat[r] + tmp):
            tmp += self._dat[r]
            r -= 1
        return r + 1 - self._size
      tmp += self._dat[r]
      if r & -r == r:
        break 
    return 0

  def __str__(self):
    ret = [self._dat[i] for i in range(1<<self._log, 1<<self._log+1)]
    return '[' + ', '.join(map(str, ret)) + ']'

  def show(self):
    ret = []
    for i in range(self._log+1):
      tmp = [' ']
      for j in range(2**i):
        tmp.append(self._dat[2**i+j])
      ret.append(' '.join(map(str, tmp)))
    print('<SegmentTree> [\n' + '\n'.join(map(str, ret)) + '\n]')



