from functools import reduce


class LazyQuadraticDivision:

  def __init__(self, n, op, mapping, composition, e, id_, V=[]):
    self.n = n
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id_ = id_

    self.size = int(self.n**.5) + 1
    self.bucket_cnt = (self.n+self.size-1) // self.size

    if not V: V = [self.e] * self.n
    self.data = [V[k*self.size:(k+1)*self.size] for k in range(self.bucket_cnt)]
    self.bucket_data = [reduce(self.op, v) for v in self.data]
    self.bucket_lazy = [self.id_] * self.bucket_cnt

  '''Change a[l:r) into x. / O(√N)'''
  def update_range(self, l: int, r: int, x) -> None:
    assert 0 <= l < r <= self.n

    def __change_data(k, l, r):
      if k >= self.bucket_cnt: return
      self.__propagate(k)
      self.data[k][l:r] = [self.mapping(x, d) for d in self.data[k][l:r]]
      self.bucket_data[k] = reduce(self.op, self.data[k])

    k1, k2 = l // self.size, r // self.size
    l, r = l-k1*self.size, r-k2*self.size
    if k1 == k2:
      __change_data(k1, l, r)
    else:
      if l == 0:
        self.bucket_lazy[k1] = self.composition(x, self.bucket_lazy[k1])
        # self.bucket_data[k1] = func(self.data[k1])
        self.bucket_data[k1] = self.mapping(x, self.bucket_data[k1])
      else:
        __change_data(k1, l, len(self.data[k1]))

      self.bucket_lazy[k1+1:k2] = [self.composition(x, bl) for bl in self.bucket_lazy[k1+1:k2]]
      # self.bucket_data[k1+1:k2] = [func(self.data[i]) for i,bd in enumerate(self.bucket_data[k1+1:k2], k1+1)]
      self.bucket_data[k1+1:k2] = [self.mapping(x, bd) for bd in self.bucket_data[k1+1:k2]]

      __change_data(k2, 0, r)

  def __propagate(self, k):
    '''propagate bucket_lazy[k]. / O(√N)'''
    if k >= self.bucket_cnt or self.bucket_lazy[k] == self.id_: return
    self.data[k] = [self.mapping(self.bucket_lazy[k], d) for d in self.data[k]]
    # self.bucket_data[k] = reduce(self.op, self.data[k])
    self.bucket_lazy[k] = self.id_

  '''Return op([l, r)). / 0 <= l <= r <= n / O(√N)'''
  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self.n

    s = self.e
    k1, k2 = l // self.size, r // self.size
    l, r = l-k1*self.size, r-k2*self.size
    self.__propagate(k1)
    self.__propagate(k2)
    if k1 == k2:
      s = reduce(self.op, self.data[k1][l:r], s)
    else:
      s = reduce(self.op, self.data[k1][l:], s)
      s = reduce(self.op, self.bucket_data[k1+1:k2], s)
      if k2 < self.bucket_cnt: s = reduce(self.op, self.data[k2][:r], s)
    return s

  '''Return op([0, n)). / O(√N)'''
  def all_prod(self):
    return reduce(self.op, self.bucket_data)

  def __getitem__(self, i):
    k = i // self.size
    self.__propagate(k)
    return self.data[k][i-k*self.size]

  def __str__(self):
    return '[' + ', '.join([str(self.__getitem__(i)) for i in range(self.n)]) + ']'


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None
id_ = None
