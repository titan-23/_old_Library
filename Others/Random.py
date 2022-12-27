class Random:
  __x, __y, __z, __w = 123456789, 362436069, 521288629, 88675123

  def __xor128(self) -> int:
    t = self.__x ^ (self.__x << 11) & 0xFFFFFFFF
    self.__x, self.__y, self.__z = self.__y, self.__z, self.__w
    self.__w = (self.__w ^ (self.__w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
    return self.__w

  def random(self) -> float:
    return self.__xor128() / 0xFFFFFFFF

  def randint(self, begin: int, end: int) -> int:
    return begin + self.__xor128() // (0xFFFFFFFF//(end+1-begin))

