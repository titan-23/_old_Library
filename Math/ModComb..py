# https://github.com/titanium-22/Library/blob/main/Math/ModComb..py


class ModComb:

  def __init__(self, limit: int, mod: int):
    self._mod = mod
    self._fact = [1, 1]
    self._factinv = [1, 1]
    self._inv = [0, 1]
    self._limit = limit
    for i in range(2, self._limit+1):
      self._fact.append(self._fact[-1]*i % self._mod)
      self._inv.append((-self._inv[self._mod%i] * (self._mod//i)) % self._mod)
      self._factinv.append(self._factinv[-1] * self._inv[-1] % self._mod)

  def ncr(self, n: int, r: int) -> int:
    '''Return (nCr % mod)'''
    if r < 0 or n < r: return 0
    return self._fact[n] * self._factinv[r] * self._factinv[n - r] % self._mod

  def nhr(self, n: int, r: int) -> int:
    return self.ncr(n+r-1, n-1)

  def ncr2(self, n: int, r: int) -> int:
    def div_mod(a: int, b: int) -> int:
      if a%b == 0:
        return a // b
      return a * pow(b, self._mod-2, self._mod) % self._mod
    ret = 1
    if r > n-r:
      r = n-r
    for i in range(r):
      ret *= n-i
      ret %= self._mod
    for i in range(1, r+1):
      ret = div_mod(ret, i)
    return ret

