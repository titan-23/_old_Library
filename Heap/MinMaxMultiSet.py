# https://github.com/titanium-22/Library/blob/main/Heap/MinMaxMultiSet.py
from typing import Generic, Iterable, TypeVar, List
from collections import Counter
T = TypeVar("T")


class MinMaxMultiSet(Generic[T]):
  # https://github.com/titanium-22/Library/blob/main/Heap/IntervalHeap.py

  def __init__(self, a: Iterable[T]=[]):
    self.data = Counter(a)
    self.heap = IntervalHeap(a)
    self.len = len(a)

  def add(self, key: T, val: int=1) -> None:
    if val == 0: return
    self.heap.add(key)
    self.data[key] += val
    self.len += val

  def discard(self, key: T, val: int=1) -> bool:
    cnt = self.data[key]
    if cnt == 0: return False
    if val >= cnt:
      self.len -= cnt
      del self.data[key]
    else:
      self.len -= val
      self.data[key] -= val
    return True

  def popleft(self) -> T:
    while True:
      v = self.heap.get_min()
      if v in self.data:
        if self.data[v] == 1:
          self.heap.pop_min()
          del self.data[v]
        else:
          self.data[v] -= 1
        self.len -= 1
        return v
      self.heap.pop_min()

  def pop(self) -> T:
    while True:
      v = self.heap.get_max()
      if v in self.data:
        self.len -= 1
        if self.data[v] == 1:
          self.heap.pop_max()
          del self.data[v]
        else:
          self.data[v] -= 1
        return v
      self.heap.pop_max()

  def get_min(self) -> T:
    while True:
      v = self.heap.get_min()
      if v in self.data:
        return v
      else:
        self.heap.pop_min()

  def get_max(self) -> T:
    while True:
      v = self.heap.get_max()
      if v in self.data:
        return v
      else:
        self.heap.pop_max()

  def to_l(self) -> List[T]:
    return sorted(self.data.elements())

  def len_elm(self) -> int:
    return len(self.data)

  def __contains__(self, key: T):
    return key in self.data

  def __getitem__(self, k: int):  # 末尾と先頭のみ
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __len__(self):
    return self.len

  def __str__(self):
    return '{' + ', '.join(map(str, sorted(self.data.elements()))) + '}'

  def __repr__(self):
    return 'MinMaxMultiSet' + str(self)

