from typing import Union, Iterable

class WordsizeTreeSet:

  def __init__(self, u: int, a=[]):
    self.u = u
    self.data = []
    self.len = 0
    if a:
      u >>= 5
      A = [0] * (u+1)
      for a_ in a:
        if A[a_>>5] * (1 << (a_&31)):
          self.len += 1
        A[a_>>5] |= 1 << (a_&31)
      self.data.append(A)
      while u:
        a = [0] * ((u>>5)+1)
        for i in range(u+1):
          if A[i]:
            a[i>>5] |= 1<<(i&31)
        self.data.append(a)
        A = a
        u >>= 5
    else:
      while u:
        u >>= 5
        self.data.append([0] * (u+1))
    self.len_data = len(self.data)
  
  def add(self, x: int) -> bool:
    if x in self: return False
    for a in self.data:
      if a[x>>5] & (1 << (x&31)): break
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
      if d >= self.len_data or x>>5 >= len(self.data[d]): return None
      m = self.data[d][x>>5] & ((~0) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) + 1
      else:
        x = (x >> 5 << 5) + (m & -m).bit_length() - 1
        if d == 0: break
        x <<= 5
        d -= 1
    return x

  def gt(self, x: int) -> Union[int, None]:
    return self.ge(x + 1)

  def le(self, x: int) -> Union[int, None]:
    d = 0
    while True:
      if x < 0 or d >= self.len_data: return None
      m = self.data[d][x>>5] & ~((~1) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) - 1
      else:
        x = (x >> 5 << 5) + m.bit_length() - 1
        if d == 0: break
        x <<= 5
        x += 31
        d -= 1
    return x

  def lt(self, x: int) -> Union[int, None]:
    return self.le(x - 1)

  def get_min(self) -> Union[int, None]:
    return self.ge(0)

  def get_max(self) -> Union[int, None]:
    return self.le(self.u - 1)

  def popleft(self) -> int:
    v = self.get_min()
    self.discard(v)
    return v

  def pop(self) -> int:
    v = self.get_max()
    self.discard(v)
    return v

  def clear(self) -> None:
    for e in self:
      self.discard(e)
    self.len = 0

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
    return 'WordsizeTreeSet(' + str(self) + ')'


class WordsizeTreeMultiSet:

  def __init__(self, u: int, a: Iterable[int]=[]):
    self.len = 0
    self.set = WordsizeTreeSet(u, a)
    cnt = {}
    for a_ in a:
      self.len += 1
      if a_ in cnt:
        cnt[a_] += 1
      else:
        cnt[a_] = 1
    self.cnt = cnt

  def add(self, x: int, val: int=1) -> None:
    self.len += val
    if x in self.cnt:
      self.cnt[x] += val
    else:
      self.cnt[x] = val
      self.set.add(x)

  def discard(self, x: int, val: int=1) -> bool:
    if x not in self.cnt: return False
    v = self.cnt[x]
    if v > val:
      self.cnt[x] -= val
      self.len -= val
    else:
      self.len -= v
      del self.cnt[x]
      self.set.discard(x)
    return True

  def count(self, x: int) -> int:
    return self.cnt[x] if x in self.cnt else 0

  def ge(self, x: int) -> Union[int, None]:
    d = 0
    ssd = self.set.data
    while True:
      if d >= len(ssd) or x>>5 >= len(ssd[d]): return None
      m = ssd[d][x>>5] & ((~0) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) + 1
      else:
        x = (x >> 5 << 5) + (m & -m).bit_length() - 1
        if d == 0: break
        x <<= 5
        d -= 1
    return x

  def gt(self, x: int) -> Union[int, None]:
    return self.ge(x + 1)

  def le(self, x: int) -> Union[int, None]:
    d = 0
    ssd = self.set.data
    while True:
      if x < 0 or d >= len(ssd): return None
      m = ssd[d][x>>5] & ~((~1) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) - 1
      else:
        x = (x >> 5 << 5) + m.bit_length() - 1
        if d == 0: break
        x <<= 5
        x += 31
        d -= 1
    return x

  def lt(self, x: int) -> Union[int, None]:
    return self.le(x - 1)

  def get_min(self) -> Union[int, None]:
    return self.ge(0)

  def get_max(self) -> Union[int, None]:
    return self.le(self.set.u - 1)

  def popleft(self) -> int:
    d = 0
    x = 0
    ssd = self.set.data
    while True:
      m = ssd[d][x>>5] & ((~0) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) + 1
      else:
        x = (x >> 5 << 5) + (m & -m).bit_length() - 1
        if d == 0: break
        x <<= 5
        d -= 1
    self.discard(x)
    return x

  def pop(self) -> int:
    d = 0
    ssd = self.set.data
    x = self.set.u - 1
    while True:
      m = ssd[d][x>>5] & ~((~1) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) - 1
      else:
        x = (x >> 5 << 5) + m.bit_length() - 1
        if d == 0: break
        x <<= 5
        x += 31
        d -= 1
    self.discard(x)
    return x

  def keys(self):
    v = self.set.get_min()
    while v is not None:
      yield v
      v = self.set.gt(v)

  def values(self):
    v = self.set.get_min()
    while v is not None:
      yield self.cnt[v]
      v = self.set.gt(v)

  def items(self):
    v = self.set.get_min()
    while v is not None:
      yield (v, self.cnt[v])
      v = self.set.gt(v)

  def clear(self) -> None:
    for e in self:
      self.set.discard(e)
    self.len = 0
    self.cnt = {}

  def __contains__(self, x: int):
    return x in self.cnt

  def __len__(self):
    return self.len

  def __iter__(self):
    v = self.set.get_min()
    while v is not None:
      for _ in range(self.cnt[v]):
        yield v
      v = self.set.gt(v)

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return 'WordsizeTreeMultiSet(' + str(self) + ')'
