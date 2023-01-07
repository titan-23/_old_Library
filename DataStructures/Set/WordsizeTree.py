from typing import Union, Iterable

class WordsizeTree:

  def __init__(self, n: int, a: Iterable[int]=[]):
    self.n = n
    self.len = 0
    self.data = []
    if a:
      n >>= 5
      A = [0] * (n+1)
      for a_ in a:
        if A[a_>>5] & 1 == 0:
          A[a_>>5] |= 1 << (a_&31)
          self.len += 1
      self.data.append(A)
      while n:
        a = [0] * ((n>>5)+1)
        for i in range(n+1):
          if self.data[-1][i]:
            a[i>>5] |= 1<<(i&31)
        self.data.append(a)
        n >>= 5
    else:
      while n:
        n >>= 5
        self.data.append([0] * (n+1))
  
  def add(self, x: int) -> bool:
    if x in self: return False
    for a in self.data:
      a[x>>5] |= 1 << (x&31)
      x >>= 5
    self.len += 1
    return True

  def discard(self, x: int) -> bool:
    if x not in self: return False
    for a in self.data:
      a[x>>5] &= ~(1 << (x&31))
      x >>= 5
      if a[x]: return
    self.len -= 1
    return True

  def ge(self, x: int) -> Union[int, None]:
    d = 0
    while True:
      if d >= len(self.data) or x>>5 >= len(self.data[d]): return None
      m = self.data[d][x>>5] & ((~0) << (x&31))
      if m == 0:
        d += 1
        x = (x>>5) + 1
      else:
        x = (x>>5<<5) + (m&-m).bit_length()-1
        if d == 0: break
        x <<= 5
        d -= 1
    return x

  def gt(self, x: int) -> Union[int, None]:
    return self.ge(x+1)

  def le(self, x: int) -> Union[int, None]:
    d = 0
    while True:
      if x < 0 or d >= len(self.data): return None
      m = self.data[d][x>>5] & ~((~1) << (x&31))
      if m == 0:
        d += 1
        x = (x>>5) - 1
      else:
        x = (x>>5<<5) + m.bit_length()-1
        if d == 0: break
        x <<= 5
        x += 31
        d -= 1
    return x

  def lt(self, x: int) -> Union[int, None]:
    return self.le(x-1)

  def get_min(self) -> Union[int, None]:
    return self.ge(0)

  def get_max(self) -> Union[int, None]:
    return self.le(self.n-1)

  def __len__(self):
    return self.len

  def __contains__(self, x: int):
    return self.data[0][x>>5] >> (x&31) & 1 == 1

  def __iter__(self):
    v = self.ge(0)
    while v is not None:
      yield v
      v = self.gt(v)

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return 'WordsizeTree' + str(self)


