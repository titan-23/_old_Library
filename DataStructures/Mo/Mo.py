from typing import Callable
from __pypy__ import newlist_hint

class Mo():

  BUCKET_SIZE = 866

  def __init__(self, n: int, q: int):
    # n:= 平方分割する列全体の大きさ
    # q:= クエリの数
    self.n = n
    self.q = q
    self.bit = max(n, q).bit_length()
    self.msk = (1 << self.bit) - 1
    self.bucket = [newlist_hint(10) for _ in range(n//Mo.BUCKET_SIZE+1)]
    self.query_count = 0

  def add_query(self, l: int, r: int) -> None:
    self.bucket[l//Mo.BUCKET_SIZE].append((((r<<self.bit)+l)<<self.bit)+self.query_count)
    self.query_count += 1

  def run(self, add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None:
    bucket, bit, msk = self.bucket, self.bit, self.msk
    for i, b in enumerate(bucket):
      b.sort(reverse=i & 1)
    nl, nr = 0, 0
    for b in bucket:
      for rli in b:
        r = rli >> bit >> bit
        l = rli >> bit & msk
        while nl > l:
          nl -= 1
          add(nl)
        while nl < l:
          delete(nl)
          nl += 1
        while nr < r:
          add(nr)
          nr += 1
        while nr > r:
          nr -= 1
          delete(nr)
        out(rli & msk)

