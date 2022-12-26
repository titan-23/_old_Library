# https://github.com/titanium-22/Library/blob/main/ProtoBitSet.py
from typing import List

class ProtoBitSet:

  TABLE = bytearray(1 << i for i in range(8))

  def __init__(self, n: int):
    self._size = (n >> 3) + 1
    self._data = bytearray(self._size)

  def add(self, k: int) -> None:
    self._data[k>>3] |= ProtoBitSet.TABLE[k & 7]

  def discard(self, k: int) -> None:
    self._data[k>>3] &= ~ProtoBitSet.TABLE[k & 7]

  def __contains__(self, k: int) -> bool:
    return self._data[k>>3] >> (k & 7) & 1 == 1

  def __getitem__(self, k: int):
    return self._data[k>>3] >> (k & 7) & 1

  def __setitem__(self, k: int, bit: bool):
    if bit:
      self._data[k>>3] |= ProtoBitSet.TABLE[k & 7]
    else:
      self._data[k>>3] &= ~ProtoBitSet.TABLE[k & 7]

  def to_l(self) -> List[int]:
    return [(i<<3)+j for i, a in enumerate(self.data) for j in range(8) if a >> j & 1 == 1]

