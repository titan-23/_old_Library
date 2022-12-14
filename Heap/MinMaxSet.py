# https://github.com/titanium-22/Library/blob/main/Heap/MinMaxSet.py
from typing import Generic, Iterable, TypeVar, List
T = TypeVar("T")


class MinMaxSet(Generic[T]):
  # https://github.com/titanium-22/Library/blob/main/Heap/IntervalHeap.py

  def __init__(self, a: Iterable[T]=[]):
    self.data = set(a)
    self.heap = IntervalHeap(self.data)

  def add(self, key: T) -> None:
    if key not in self.data:
      self.heap.add(key)
      self.data.add(key)

  def discard(self, key: T) -> bool:
    if key in self.data:
      self.data.discard(key)
      return True
    return False

  def popleft(self) -> T:
    while True:
      v = self.heap.pop_min()
      if v in self.data:
        self.data.discard(v)
        return v

  def pop(self) -> T:
    while True:
      v = self.heap.pop_max()
      if v in self.data:
        self.data.discard(v)
        return v

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
    return sorted(self.data)

  def len_elm(self) -> int:
    return len(self.data)

  def __contains__(self, key: T):
    return key in self.data

  def __getitem__(self, k: int):  # 末尾と先頭のみ
    if k == -1 or k == len(self.data)-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __len__(self):
    return len(self.data)

  def __str__(self):
    return '{' + ', '.join(map(str, sorted(self.data))) + '}'

  def __repr__(self):
    return 'MinMaxSet' + str(self)

