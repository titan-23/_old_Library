# https://github.com/titanium-22/Library/blob/main/SparseTable/SparseTableRMQ.py


from typing import Generic, TypeVar, Iterable, Callable
T = TypeVar("T")


class SparseTableRMQ(Generic[T]):

  def __init__(self, a: Iterable[T]) -> None:
    a = list(a)
    self.size = len(a)
    log = self.size.bit_length()
    self.data = [None] * log
    self.data[0] = a
    for i in range(log-1):
      pre = self.data[i]
      l = 1 << i
      self.data[i+1] = [pre[j] if pre[j] < pre[j+l] else pre[j+l] for j in range(len(pre)-l)]
    if len(a) == 0: return
    self.e = max(a)

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.size
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.data[u][l] if self.data[u][l] < self.data[u][r-(1<<u)] else self.data[u][r-(1<<u)]

  def __getitem__(self, k: int) -> T:
    assert 0 <= k < self.size
    return self.data[0][k]

  def __str__(self):
    return '[' +  ', '.join(map(str, self.data[0])) + ']'

  def __repr__(self):
    return 'SparseTableRMQ ' + str(self)


