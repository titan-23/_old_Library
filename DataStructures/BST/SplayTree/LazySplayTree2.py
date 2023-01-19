import sys
from array import array
from typing import Generic, List, TypeVar, Tuple, Callable, Iterable, Union
T = TypeVar("T")
F = TypeVar("F")

class LazySplayTree(Generic[T, F]):

  key = [None]
  data = [None]
  lazy = [None]
  size = array('I', [0])
  left = array('I', [0])
  right = array('I', [0])
  rev = array('i', [0])
  end = 1

  @staticmethod
  def reserve(n):
    d1 = [0] * n
    d2 = [None] * n
    a = array('I', d1)
    LazySplayTree.key += d2
    LazySplayTree.data += d2
    LazySplayTree.lazy += d2
    LazySplayTree.size += array('I', [1] * n)
    LazySplayTree.left += a
    LazySplayTree.right += a
    LazySplayTree.rev += array('i', d1)

  def __init__(self, a: Iterable[T]=[], op: Callable[[T, T], T]=lambda x,y: None, mapping: Callable[[F, T], T]=None, composition: Callable[[F, F], F]=None, e: T=None, node: int=0):
    self.node = node
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        LazySplayTree.left[mid] = sort(l, mid)
      if mid+1 != r:
        LazySplayTree.right[mid] = sort(mid+1, r)
      self._update(mid)
      return mid
    n = len(a)
    key, data = LazySplayTree.key, LazySplayTree.data
    end = LazySplayTree.end
    LazySplayTree.end += n
    LazySplayTree.reserve(n)
    for i in range(n):
      key[end+i] = a[i]
      data[end+i] = a[i]
    self.node = sort(end, n+end)

  def _propagate(self, node: int) -> None:
    if LazySplayTree.rev[node]:
      LazySplayTree.left[node], LazySplayTree.right[node] = LazySplayTree.right[node], LazySplayTree.left[node]
      lnode, rnode = LazySplayTree.left[node], LazySplayTree.right[node]
      if lnode != 0:
        LazySplayTree.rev[lnode] ^= 1
      if rnode != 0:
        LazySplayTree.rev[rnode] ^= 1
      LazySplayTree.rev[node] = 0
    lnode, rnode = LazySplayTree.left[node], LazySplayTree.right[node]
    lazy = LazySplayTree.lazy[node]
    if lazy is not None:
      if lnode != 0:
        LazySplayTree.data[lnode] = self.mapping(lazy, LazySplayTree.data[lnode])
        LazySplayTree.key[lnode] = self.mapping(lazy, LazySplayTree.key[lnode])
        LazySplayTree.lazy[lnode] = lazy if LazySplayTree.lazy[lnode] is None else self.composition(lazy, LazySplayTree.lazy[lnode])
      if rnode != 0:
        LazySplayTree.data[rnode] = self.mapping(lazy, LazySplayTree.data[rnode])
        LazySplayTree.key[rnode] = self.mapping(lazy, LazySplayTree.key[rnode])
        LazySplayTree.lazy[rnode] = lazy if LazySplayTree.lazy[rnode] is None else self.composition(lazy, LazySplayTree.lazy[rnode])
      LazySplayTree.lazy[node] = None

  def _update(self, node: int) -> None:
    lnode, rnode = LazySplayTree.left[node], LazySplayTree.right[node]
    LazySplayTree.size[node] = 1 + LazySplayTree.size[lnode] + LazySplayTree.size[rnode]
    if lnode == 0:
      if rnode == 0:
        LazySplayTree.data[node] = LazySplayTree.key[node]
      else:
        LazySplayTree.data[node] = self.op(LazySplayTree.key[node], LazySplayTree.data[rnode])
    else:
      if rnode == 0:
        LazySplayTree.data[node] = self.op(LazySplayTree.data[lnode], LazySplayTree.key[node])
      else:
        LazySplayTree.data[node] = self.op(self.op(LazySplayTree.data[lnode], LazySplayTree.key[node]), LazySplayTree.data[rnode])

  def _splay(self, path: List[int], di: int) -> int:
    left, right = LazySplayTree.left, LazySplayTree.right
    while len(path) > 1:
      node = path.pop()
      pnode = path.pop()
      if di & 1:
        tmp = left[node]
        left[node] = right[tmp]
        if di >> 1 & 1:
          right[tmp] = node
          left[pnode] = right[node]
          right[node] = pnode
        else:
          right[pnode] = left[tmp]
          right[tmp] = node
          left[tmp] = pnode
      else:
        tmp = right[node]
        right[node] = left[tmp]
        if di >> 1 & 1:
          left[pnode] = right[tmp]
          left[tmp] = node
          right[tmp] = pnode
        else:
          left[tmp] = node
          right[pnode] = left[node]
          left[node] = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      di >>= 2
      if di & 1:
        left[path[-1]] = tmp
      else:
        right[path[-1]] = tmp
    gnode = path[0]
    if di & 1:
      node = left[gnode]
      left[gnode] = right[node]
      right[node] = gnode
    else:
      node = right[gnode]
      right[gnode] = left[node]
      left[node] = gnode
    self._update(gnode)
    self._update(node)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    size = LazySplayTree.size
    node = self.node
    if k < 0: k += size[node]
    left, right = LazySplayTree.left, LazySplayTree.right
    di = 0
    path = []
    while True:
      self._propagate(node)
      t = size[left[node]]
      if t == k:
        if path:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di <<= 1
        di |= 1
        node = left[node]
      else:
        path.append(node)
        di <<= 1
        node = right[node]
        k -= t + 1

  def _get_min_splay(self, node: int) -> Union[int, None]:
    if node == 0: return None
    self._propagate(node)
    left = LazySplayTree.left
    if left[node] == 0: return node
    path = []
    while left[node] != 0:
      path.append(node)
      node = left[node]
      self._propagate(node)
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: int) -> Union[int, None]:
    if node == 0: return None
    self._propagate(node)
    right = LazySplayTree.right
    if right[node] == 0: return node
    path = []
    while right[node] != 0:
      path.append(node)
      node = right[node]
      self._propagate(node)
    return self._splay(path, 0)

  def merge(self, other: "LazySplayTree") -> None:
    if self.node == 0:
      self.node = other.node
      return
    if other.node == 0:
      return
    self.node = self._get_max_splay(self.node)
    LazySplayTree.right[self.node] = other.node
    self._update(self.node)

  def split(self, k: int) -> Tuple["LazySplayTree", "LazySplayTree"]:
    if k >= LazySplayTree.size[self.node]:
      return self, LazySplayTree(op=self.op, mapping=self.mapping, composition=self.composition, e=self.e)
    self._set_kth_elm_splay(k)
    left = LazySplayTree(op=self.op, mapping=self.mapping, composition=self.composition, e=self.e, node=LazySplayTree.left[self.node])
    LazySplayTree.left[self.node], right = 0, self
    self._update(right.node)
    return left, right

  def reverse(self, l: int, r: int) -> None:
    if l >= r: return
    left, right = self.split(r)
    if l == 0:
      LazySplayTree.rev[left.node] ^= 1
    else:
      left._set_kth_elm_splay(l-1)
      LazySplayTree.rev[LazySplayTree.right[left.node]] ^= 1
    if right.node == 0:
      right.node = left.node
    else:
      LazySplayTree.left[right.node] = left.node
      self._update(right.node)
    self.node = right.node

  def all_reverse(self) -> None:
    if self.node == 0: return
    LazySplayTree.rev[self.node] ^= 1

  def apply(self, l: int, r: int, f: F) -> None:
    if l >= r: return
    left, right = self.split(r)
    if l == 0:
      lnode = left.node
      LazySplayTree.key[lnode] = self.mapping(f, LazySplayTree.key[lnode])
      LazySplayTree.data[lnode] = self.mapping(f, LazySplayTree.data[lnode])
      LazySplayTree.lazy[lnode] = f if LazySplayTree.lazy[lnode] is None else self.composition(f, LazySplayTree.lazy[lnode])
    else:
      left._set_kth_elm_splay(l-1)
      lnode = left.node
      node = LazySplayTree.right[lnode]
      LazySplayTree.key[node] = self.mapping(f, LazySplayTree.key[node])
      LazySplayTree.data[node] = self.mapping(f, LazySplayTree.data[node])
      LazySplayTree.lazy[node] = f if LazySplayTree.lazy[node] is None else self.composition(f, LazySplayTree.lazy[node])
      self._update(lnode)
    if right.node == 0:
      right.node = lnode
    else:
      LazySplayTree.left[right.node] = lnode
      self._update(right.node)
    self.node = right.node

  def all_apply(self, f: F) -> None:
    LazySplayTree.key[self.node] = self.mapping(f, LazySplayTree.key[self.node])
    LazySplayTree.data[self.node] = self.mapping(f, LazySplayTree.data[self.node])
    LazySplayTree.lazy[self.node] = f if LazySplayTree.lazy[self.node] is None else self.composition(f, LazySplayTree.lazy[self.node])

  def prod(self, l: int, r: int) -> T:
    if l >= r: return self.e
    left, right = self.split(r)
    if l == 0:
      res = LazySplayTree.data[left.node]
    else:
      left._set_kth_elm_splay(l-1)
      res = LazySplayTree.data[LazySplayTree.right[left.node]]
    if right.node == 0:
      right.node = left.node
    else:
      LazySplayTree.left[right.node] = left.node
      self._update(right.node)
    self.node = right.node
    return res

  def all_prod(self) -> T:
    return self.e if self.node == 0 else LazySplayTree.data[self.node]

  def _make_node(self, key: T) -> int:
    end = LazySplayTree.end
    if end >= len(LazySplayTree.key):
      LazySplayTree.key.append(key)
      LazySplayTree.data.append(key)
      LazySplayTree.lazy.append(None)
      LazySplayTree.size.append(1)
      LazySplayTree.left.append(0)
      LazySplayTree.right.append(0)
      LazySplayTree.rev.append(0)
    else:
      LazySplayTree.key[end] = key
      LazySplayTree.data[end] = key
    LazySplayTree.end += 1
    return end

  def insert(self, k: int, key: T) -> None:
    node = self._make_node(key)
    if self.node == 0:
      self.node = node
      return
    if k >= LazySplayTree.size[self.node]:
      self._set_kth_elm_splay(LazySplayTree.size[self.node]-1)
      LazySplayTree.left[node] = self.node
      self.node = node
    else:
      self._set_kth_elm_splay(k)
      if LazySplayTree.left[self.node] != 0:
        LazySplayTree.left[node] = LazySplayTree.left[self.node]
        LazySplayTree.left[self.node] = 0
        self._update(self.node)
      LazySplayTree.right[node] = self.node
      self.node = node
    self._update(self.node)

  def append(self, key: T) -> None:
    if self.node == 0:
      self.node = self._make_node(key)
      return
    node = self._get_max_splay(self.node)
    self.node = self._make_node(key)
    LazySplayTree.left[self.node] = node
    self._update(self.node)

  def appendleft(self, key: T) -> None:
    if self.node == 0:
      self.node = self._make_node(key)
      return
    node = self._get_min_splay(self.node)
    self.node = self._make_node(key)
    LazySplayTree.right[self.node] = node
    self._update(self.node)

  def pop(self, k: int=-1) -> T:
    if k == -1:
      node = self._get_max_splay(self.node)
      self._propagate(node)
      self.node = LazySplayTree.left[node]
      return LazySplayTree.key[node]
    self._set_kth_elm_splay(k)
    res = LazySplayTree.key[self.node]
    if LazySplayTree.left[self.node] == 0:
      self.node = LazySplayTree.right[self.node]
    elif LazySplayTree.right[self.node] == 0:
      self.node = LazySplayTree.left[self.node]
    else:
      node = self._get_max_splay(LazySplayTree.left[self.node])
      LazySplayTree.right[node] = LazySplayTree.right[self.node]
      self.node = node
      self._update(self.node)
    return res

  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self._propagate(node)
    self.node = LazySplayTree.right[node]
    return LazySplayTree.key[node]

  def to_l(self) -> List[T]:
    a = []
    if self.node == 0:
      return a
    if sys.getrecursionlimit() < LazySplayTree.size[self.node]:
      sys.setrecursionlimit(LazySplayTree.size[self.node]+1)
    left, right, key = LazySplayTree.left, LazySplayTree.right, LazySplayTree.key
    def rec(node):
      self._propagate(node)
      if left[node] != 0:
        rec(left[node])  
      a.append(key[node])
      if right[node] != 0:
        rec(right[node])
    rec(self.node)
    return a

  def clear(self) -> None:
    self.node = 0

  def __setitem__(self, k: int, key: T):
    self._set_kth_elm_splay(k)
    LazySplayTree.key[self.node] = key
    self._update(self.node)

  def __getitem__(self, k: int) -> T:
    if k < 0 or k >= LazySplayTree.size[self.node]: raise IndexError
    self._set_kth_elm_splay(k)
    return LazySplayTree.key[self.node]

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == LazySplayTree.size[self.node]:
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(LazySplayTree.size[self.node]):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return LazySplayTree.size[self.node]

  def __str__(self):
    return '[' + ', '.join(map(str, self.to_l())) + ']'

  def __bool__(self):
    return self.node != 0

  def __repr__(self):
    return 'LazySplayTree' + str(self)


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

