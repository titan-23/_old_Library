# https://github.com/titanium-22/Library/blob/main/FenwickTreeSet.py


from typing import Iterable, Set, TypeVar, Generic, Union, Tuple
T = TypeVar("T")


class FenwickTreeSet(Generic[T]):

  # Build a new FenwickTreeSet. / O(len(A) log(len(A)))
  def __init__(self, _used: Set[T], _a: Iterable[T]=[], _multi=False):
    # used: used values(distinct); a: init values

    _used = sorted(_used)
    self._len = 0
    self._size = len(_used)
    self._to_zaatsu = _used if _used[-1] == self._size-1 else {key: i for i, key in enumerate(_used)}
    self._to_origin = _used
    self._cnt = [0] * self._size
    if _a:
      a_ = [0] * self._size
      for v in _a:
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

  def add(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i] == 0:
      self._len += 1
      self._cnt[i] = 1
      self._fw.add(i, 1)
      return True
    return False

  def remove(self, key: T) -> None:
    if self.discard(key): return
    raise KeyError(key)

  def discard(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i] == 0: return False
    self._len -= 1
    self._cnt[i] = 0
    self._fw.add(i, -1)
    return True

  def count(self, key: T) -> int:
    return self._cnt[self._to_zaatsu[key]]

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      return key
    pref = self._fw.pref(i - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    pref = self._fw.pref(self._to_zaatsu[key] - 1) - 1
    return None if pref < 0 else self.__getitem__(pref)

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    i = self._to_zaatsu[key]
    if self._cnt[i] > 0:
      return key
    pref = self._fw.pref(i)
    return None if pref >= self._len else self.__getitem__(pref)

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    pref = self._fw.pref(self._to_zaatsu[key])
    return None if pref >= self._len else self.__getitem__(pref)

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key: T) -> int:
    return self._fw.pref(self._to_zaatsu[key] - 1)

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key: T) -> int:
    return self._fw.pref(self._to_zaatsu[key])

  def pop(self, k: int=-1) -> T:
    if k < 0:
      k += self._len
    self._len -= 1
    i = 0
    acc = 0
    s = self._fw._s
    while s:
      if i+s <= self._size:
        if acc + self._fw._tree[i+s] <= k:
          acc += self._fw._tree[i+s]
          i += s
        else:
          self._fw._tree[i+s] -= 1
      s >>= 1
    self._cnt[i] -= 1
    return self._to_origin[i]

  def popleft(self) -> T:
    return self.pop(0)

  def __getitem__(self, k):
    if k < 0:
      k += self._len
    return self._to_origin[self._fw.bisect_right(k)]

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

  def __contains__(self, key: T):
    return self._cnt[self._to_zaatsu[key]] > 0

  def __bool__(self):
    return self._len > 0


class FenwickTreeMultiSet(FenwickTreeSet, Generic[T]):

  def __init__(self, used: Set[T], a: Iterable[T]=[]) -> None:
    super().__init__(used, a, _multi=True)

  def add(self, key: T, num: int=1) -> None:
    if num <= 0: return
    i = self._to_zaatsu[key]
    self._len += num
    self._cnt[i] += num
    self._fw.add(i, num)

  def discard(self, key: T, num: int=1) -> bool:
    cnt = self.count(key)
    if num > cnt:
      num = cnt
    if num <= 0: return False
    i = self._to_zaatsu[key]
    self._len -= num
    self._cnt[i] -= num
    self._fw.add(i, -num)
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, num=self.count(key))

  def items(self) -> Iterable[Tuple[T, int]]:
    _iter = 0
    while _iter < self._len:
      res = self.__getitem__(_iter)
      cnt = self.count(res)
      _iter += cnt
      yield res, cnt

  def show(self) -> None:
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')

  def __repr__(self):
    return 'FenwickTreeMultiSet ' + str(self)

