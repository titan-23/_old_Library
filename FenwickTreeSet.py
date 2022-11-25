# https://github.com/titanium-22/Library/blob/main/FenwickTreeSet.py


class FenwickTreeSet:
  
  # Build a new FenwickTreeSet. / O(len(A) log(len(A)))
  def __init__(self, _used: set, _a=[], _multi=False):
    # used: used values(distinct); a: init values

    _used = sorted(_used)
    self._len = 0
    self._size = len(_used)

    if _used[-1] != self._size - 1:
      self._to_zaatsu = {x: i for i, x in enumerate(_used)}
    else:
      self._to_zaatsu = _used
    self._to_origin = _used

    self._cnt = [0] * self._size

    if a:
      a_ = [0] * self._size
      for v in a:
        i = self._to_zaatsu[v]
        if _multi:
          self._len += 1
          a_[i] += 1
          self._cnt[i] += 1
        elif a_[i] == 0:
          self._len += 1
          a_[i] = 1
          self._cnt[i] = 1
      self._fw = FenwickTree(a_)
    else:
      self._fw = FenwickTree(self._size)

  '''Add x. / O(logN)'''
  def add(self, key) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i] == 0:
      self._len += 1
      self._cnt[i] = 1
      self._fw.add(i, 1)
      return True
    return False

  '''Remove x. / O(logN)'''
  def remove(self, key) -> bool:
    if self.discard(key):
      return True
    raise KeyError(key)

  '''Discard x. / O(logN)'''
  def discard(self, key) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i] == 0:
      return False
    self._len -= 1
    self._cnt[i] = 0
    self._fw.add(i, -1)
    return True

  '''Return the number of key. / O(logN)'''
  def count(self, key) -> int:
    return self._cnt[self._to_zaatsu[key]]

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      return key
    pref = self._fw.pref(i - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    pref = self._fw.pref(self._to_zaatsu[key] - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    i = self._to_zaatsu[key]
    if self._cnt[i] > 0:
      return key
    pref = self._fw.pref(i)
    return None if pref >= self._len else self.__getitem__(pref)

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    pref = self._fw.pref(self._to_zaatsu[key])
    return None if pref >= self._len else self.__getitem__(pref)

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key) -> int:
    return self._fw.pref(self._to_zaatsu[key] - 1)

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    return self._fw.pref(self._to_zaatsu[key])

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p=-1):
    if p < 0:
      p += self._len
    self._len -= 1
    i, acc, s = 0, 0, self._fw._s
    while s:
      if i + s <= self._size:
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
    return self._to_origin[self._fw.bisect_right(x)]

  def __repr__(self):
    return 'FenwickTreeSet ' + str(self)

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

  def __contains__(self, x):
    return self._cnt[self._to_zaatsu[x]] > 0

  def __bool__(self):
    return self._len > 0


class FenwickTreeMultiSet(FenwickTreeSet):

  def __init__(self, used: set, a=[]) -> None:
    super().__init__(used, a, _multi=True)

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
    return self.discard(x, num=self.count(x))

  '''Yield (key, val). / O(NlogN)'''
  def items(self) -> tuple:
    _iter = 0
    while _iter < self._len:
      res = self.__getitem__(_iter)
      cnt = self.count(res)
      _iter += cnt
      yield (res, cnt)

  def show(self):
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')

  def __repr__(self):
    return 'FenwickTreeMultiSet ' + str(self)

