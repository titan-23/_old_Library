# def __init__(self, n, op=lambda x,y: x+y, default=0, V=[]):
class SegmentTree_Range_Add_Query:

  def __init__(self, n, op=lambda x,y: x+y, default=0, V=[]):
    "Make a new Segment Tree. / 0 <= n <= 10**8. / O(N)" # default=lambda x:0
    assert 0 <= n <= 10**8
    self._n       = n
    self._log     = (n-1).bit_length()
    self._size    = 2 ** self._log
    self._op      = op
    self._default = default
    self._dat     = [self._default] * (2*self._size)
    if V:
      for i in range(self._n):
        self._dat[self._size+i] = V[i]


  def get(self, p: int):
    "Get a[p]. / O(logN)"
    assert 0 <= p <= self._size
    p += self._size
    res = self._dat[p]
    for i in range(self._log):
      p >>= 1
      res += self._dat[p]
    return res

  def __getitem__(self, p: int):
    "Get a[p]. / O(logN)"
    return self.get(p)

  def add(self, l: int, r: int, x):
    "Return op([l, r)). / 0 <= l <= r <= n / O(logN)"
    assert 0 <= l <= r <= self._n
    l += self._size
    r += self._size
    lres, rres = self._default, self._default
    while l < r:
      if l & 1:
        self._dat[l] = self._op(self._dat[l], x)
        l += 1
      if r & 1:
        r -= 1
        self._dat[r] = self._op(self._dat[r], x)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self):
    "Return op([0, n)). / O(1)"
    return self._dat[1]

  def __str__(self):
    ret = []
    for i in range(self._log+1):
      tmp = [' ']
      for j in range(2**i):
        tmp.append(self._dat[2**i+j])
      ret.append(' '.join(map(str, tmp)))
    return '<SegmentTree> [\n' + '\n'.join(map(str, ret)) + '\n]'

