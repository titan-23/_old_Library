from typing import Iterable, Hashable
from collections import Counter


class HashedMultiSet:

  def __init__(self, a: Iterable[Hashable]=[]) -> None:
    self._data = Counter(a)
    self._len = len(a)

  def add(self, key: Hashable, val: int=1) -> None:
    self._data[key] += val
    self._len += val

  def discard(self, key: Hashable, val: int=1) -> None:
    if self._data[key] > val:
      self._len -= val
      self._data[key] -= val
    else:
      self._len -= self._data[key]
      del self._data[key]

  def discard_all(self, key: Hashable) -> None:
    self._len -= self._data[key]
    del self._data[key]

  def len_elm(self) -> int:
    return len(self._data)

  def keys(self):
    for k in self._data.keys():
      yield k

  def values(self):
    for v in self._data.values():
      yield v

  def items(self):
    for item in self._data.items():
      yield item

  def clear(self):
    self._data = Counter()
    self._len = 0
    self._len_elm = 0

  def __contains__(self, key: Hashable):
    return key in self._data

  def __len__(self):
    return self._len

