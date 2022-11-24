class IntervalHeap:

  def __init__(self, _V=[]):
    self._data = list(_V)
    self._heapify()

  def _heapify(self):
    n = len(self._data)
    for i in range(n-1, -1, -1):
      if i & 1 and self._data[i-1] < self._data[i]:
        self._data[i-1], self._data[i] = self._data[i], self._data[i-1]
      k = self._down(i)
      self._up(k, i)
  
  '''Add x. / O(logN)'''
  def heappush(self, x):
    self._data.append(x)
    self._up(len(self._data)-1)

  '''Delete and Return min element. / O(logN)'''
  def heappop_min(self):
    if len(self._data) < 3:
      res = self._data.pop()
    else:
      self._data[1], self._data[-1] = self._data[-1], self._data[1]
      res = self._data.pop()
      k = self._down(1)
      self._up(k)
    return res

  '''Delete and Return max element. / O(logN)'''
  def heappop_max(self):
    if len(self._data) < 2:
      res = self._data.pop()
    else:
      self._data[0], self._data[-1] = self._data[-1], self._data[0]
      res = self._data.pop()
      self._up(self._down(0))
    return res

  '''Return min element. / O(1)'''
  def heapget_min(self):
    return self._data[0] if len(self._data) < 2 else self._data[1]

  '''Return max element. / O(1)'''
  def heapget_max(self):
    return self._data[0]

  def __len__(self):
    return len(self._data)

  def __bool__(self):
    return len(self._data) > 0

  def _parent(self, k):
    return ((k>>1)-1) & ~1

  def _down(self, k):
    n = len(self._data)
    if k & 1:
      while 2*k+1 < n:
        c = 2*k+3
        if n <= c or self._data[c-2] < self._data[c]:
          c -= 2
        if c < n and self._data[c] < self._data[k]:
          self._data[k], self._data[c] = self._data[c], self._data[k]
          k = c
        else:
          break
    else:
      while 2*k+2 < n:
        c = 2*k+4
        if n <= c or self._data[c] < self._data[c-2]:
          c -= 2
        if c < n and self._data[k] < self._data[c]:
          self._data[k], self._data[c] = self._data[c], self._data[k]
          k = c
        else:
          break
    return k

  def _up(self, k, root=1):
    if (k|1) < len(self._data) and self._data[k&~1] < self._data[k|1]:
      self._data[k&~1], self._data[k|1] = self._data[k|1], self._data[k&~1]
      k ^= 1
    while root < k:
      p = self._parent(k)
      if not self._data[p] < self._data[k]:
        break
      self._data[p], self._data[k] = self._data[k], self._data[p]
      k = p
    while root < k:
      p = self._parent(k) | 1
      if not self._data[k] < self._data[p]:
        break
      self._data[p], self._data[k] = self._data[k], self._data[p]
      k = p
    return k

  def __str__(self):
    return '[' + ', '.join(map(str, sorted(self._data))) + ']'


