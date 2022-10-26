class FenwickTreeSet:
  
  # Build a new FenwickTreeSet. / O(len(A) log(len(A)))
  def __init__(self, A: set, V=[], _multi=False):
    # A: used values(distinct)(needed); V: init values

    __A = sorted(A)
    self._len = 0
    self.__size = len(__A)

    if __A[-1] != self.__size - 1:
      self._to_zaatsu = {x: i for i, x in enumerate(__A)}
    else:
      self._to_zaatsu = __A
    self._to_origin = __A

    self._cnt = [0] * self.__size

    if V:
      VV = [0] * self.__size
      for v in V:
        i = self._to_zaatsu[v]
        if _multi:
          self._len += 1
          VV[i] += 1
          self._cnt[i] += 1
        elif VV[i] == 0:
          self._len += 1
          VV[i] = 1
          self._cnt[i] = 1
      self._fw = FenwickTree(self.__size, V=VV)
    else:
      self._fw = FenwickTree(self.__size)

  '''Add x. / O(logN)'''
  def add(self, x) -> bool:
    i = self._to_zaatsu[x]
    if self._cnt[i] == 0:
      self._len += 1
      self._cnt[i] = 1
      self._fw.add(i, 1)
      return True
    return False

  '''Remove x. / O(logN)'''
  def remove(self, x) -> bool:
    if self.discard(x):
      return True
    raise KeyError(x)

  '''Discard x. / O(logN)'''
  def discard(self, x) -> bool:
    i = self._to_zaatsu[x]
    if self._cnt[i] == 0:
      return False
    self._len -= 1
    self._cnt[i] = 0
    self._fw.add(i, -1)
    return True

  '''Return the number of x. / O(logN)'''
  def count(self, x) -> int:
    return self._cnt[self._to_zaatsu[x]]

  '''Find the largest element <= x, or None if it doesn't exist. / O(logN)'''
  def le(self, x):
    i = self._to_zaatsu[x]
    if self._cnt[i]:
      return x
    pref = self._fw.pref(i - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the largest element < x, or None if it doesn't exist. / O(logN)'''
  def lt(self, x):
    pref = self._fw.pref(self._to_zaatsu[x] - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the smallest element >= x, or None if it doesn't exist. / O(logN)'''
  def ge(self, x):
    i = self._to_zaatsu[x]
    if self._cnt[i] > 0:
      return x
    pref = self._fw.pref(i)
    return None if pref >= self._len else self.__getitem__(pref)

  '''Find the smallest element > x, or None if it doesn't exist. / O(logN)'''
  def gt(self, x):
    pref = self._fw.pref(self._to_zaatsu[x])
    return None if pref >= self._len else self.__getitem__(pref)

  '''Count the number of elements < x. / O(logN)'''
  def index(self, x) -> int:
    return self._fw.pref(self._to_zaatsu[x] - 1)

  '''Count the number of elements <= x. / O(logN)'''
  def index_right(self, x) -> int:
    return self._fw.pref(self._to_zaatsu[x])

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p=-1):
    if p < 0:
      p += self._len
    self._len -= 1
    i, acc, s = 0, 0, 1 << self._fw._depth
    while s:
      if i + s <= self.__size:
        if acc + self._fw._tree[i + s] <= p:
          acc += self._fw._tree[i + s]
          i += s
        else:
          self._fw._tree[i + s] -= 1
      s >>= 1
    self._cnt[i] -= 1
    return self._to_origin[i]

  '''Return and Remove min element. / O(logN)'''
  def popleft(self):
    return self.pop(0)

  def __getitem__(self, x):
    if x < 0:
      x += self._len
    if 0 <= x < self._len:
      return self._to_origin[self._fw.bisect_right(x)]
    raise IndexError

  def __repr__(self):
    # return '<FenwickTreeSet> {' + ', '.join(map(str, self)) + '}'
    return self.__str__()

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self._len:
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self._len):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return self._len

  def __contains__(self, x):
    return self._cnt[self._to_zaatsu[x]] > 0

  def __bool__(self):
    return self._len > 0


class FenwickTreeMultiSet(FenwickTreeSet):

  def __init__(self, A: set, V=[]) -> None:
    super().__init__(A, V=V, _multi=True)  # A: set or HashSet

  '''Add x. / O(logN)'''
  def add(self, x: int, num=1) -> None:
    if num <= 0:
      return
    self._len += num
    i = self._to_zaatsu[x]
    self._cnt[i] += num
    self._fw.add(i, num)

  '''Discard x. / O(logN)'''
  def discard(self, x: int, num=1) -> bool:
    cnt = self.count(x)
    if num > cnt:
      num = cnt
    if num <= 0:
      return False
    i = self._to_zaatsu[x]
    self._len -= num
    self._cnt[i] -= num
    self._fw.add(i, -num)
    return True

  '''Discard all x. / O(logN)'''
  def discard_all(self, x: int) -> bool:
    return self.discard(x, num=super().count(x))

  '''Yield (key, val). / O(NlogN)'''
  def items(self) -> tuple:
    __iter = 0
    while __iter < self._len:
      res = self.__getitem__(__iter)
      cnt = super().count(res)
      __iter += cnt
      yield (res, cnt)

  def show(self):
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')

  def __repr__(self):
    return self.__str__()

