# https://github.com/titanium-22/Library/blob/main/SparseTable.py


from typing import Generic, TypeVar, Iterable, Callable
T = TypeVar("T")


class SparseTable(Generic[T]):

  def __init__(self, a: Iterable[T], op: Callable[[T, T], T], e: T=None) -> None:
    a = list(a)
    n = len(a)
    log = n.bit_length()
    data = [None] * log
    data[0] = a
    for i in range(log-1):
      pre = data[i]
      l = 1 << i
      data[i+1] = [op(pre[j], pre[j+l]) for j in range(len(pre)-l)]
    self.data = data
    self.op = op
    self.e = e

  def prod(self, l: int, r: int) -> T:
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.op(self.data[u][l], self.data[u][r-(1<<u)])

  def __getitem__(self, k: int) -> T:
    return self.data[0][k]

  def __str__(self):
    return '[' +  ', '.join(map(str, self.data[0])) + ']'

  def __repr__(self):
    return 'SparseTable ' + str(self)


