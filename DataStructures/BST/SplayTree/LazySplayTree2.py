from array import array
from typing import Generic, List, TypeVar, Tuple, Callable, Iterable, Optional, Union
from __pypy__ import newlist_hint
T = TypeVar('T')
F = TypeVar('F')

class MonoidData(Generic[T, F]):

  def __init__(self, op: Optional[Callable[[T, T], T]]=None, \
              mapping: Optional[Callable[[F, T], T]]=None, \
              composition: Optional[Callable[[F, F], F]]=None, \
              e: T=None, id: F=None):
    self.op = (lambda s, t: e) if op is None else op
    self.mapping = (lambda f, s: e) if op is None else mapping
    self.composition = (lambda f, g: id) if op is None else composition
    self.e = e
    self.id = id
    self.keydata: List[T] = [e, e]
    self.lazy: List[F] = [id]
    self.size: array[int] = array('I', bytes(4))
    self.child: array[int] = array('I', bytes(8))
    self.rev: array[int] = array('B', bytes(1))
    self.end: int = 1

  def reserve(self, n: int) -> None:
    if n <= 0: return
    self.keydata += [self.e] * (2 * n)
    self.lazy += [self.id] * n
    self.size += array('I', [1] * n)
    self.child += array('I', bytes(8 * n))
    self.rev += array('B', bytes(n))

class LazySplayTree(Generic[T, F]):

  def __init__(self, monoiddata: 'MonoidData', n_or_a: Union[int, Iterable[T]]=0, _node: int=0):
    self.monoiddata = monoiddata
    self.node = _node
    if isinstance(n_or_a, int):
      a = [monoiddata.e for _ in range(n_or_a)]
    elif not hasattr(n_or_a, '__len__'):
      a = list(n_or_a)
    else:
      a = n_or_a
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        child[mid<<1] = sort(l, mid)
      if mid + 1 != r:
        child[mid<<1|1] = sort(mid+1, r)
      self._update(mid)
      return mid
    n = len(a)
    keydata, child = self.monoiddata.keydata, self.monoiddata.child
    end = self.monoiddata.end
    self.monoiddata.reserve(n+end-len(keydata)//2+1)
    self.monoiddata.end += n
    for i, e in enumerate(a):
      keydata[end+i<<1] = e
      keydata[end+i<<1|1] = e
    self.node = sort(end, n+end)

  def _make_node(self, key: T) -> int:
    monoiddata = self.monoiddata
    if monoiddata.end >= len(monoiddata.size):
      monoiddata.keydata.append(key)
      monoiddata.keydata.append(key)
      monoiddata.lazy.append(monoiddata.id)
      monoiddata.size.append(1)
      monoiddata.child.append(0)
      monoiddata.child.append(0)
      monoiddata.rev.append(0)
    else:
      monoiddata.keydata[monoiddata.end<<1] = key
      monoiddata.keydata[monoiddata.end<<1|1] = key
    monoiddata.end += 1
    return monoiddata.end - 1

  def _propagate(self, node: int) -> None:
    monoiddata = self.monoiddata
    rev, child = monoiddata.rev, monoiddata.child
    if rev[node]:
      child[node<<1], child[node<<1|1] = child[node<<1|1], child[node<<1]
      rev[node] = 0
      rev[child[node<<1]] ^= 1
      rev[child[node<<1|1]] ^= 1
    nlazy = monoiddata.lazy[node]
    if nlazy == monoiddata.id:
      return
    lnode, rnode = child[node<<1], child[node<<1|1]
    keydata, lazy = monoiddata.keydata, monoiddata.lazy
    lazy[node] = monoiddata.id
    if lnode:
      lazy[lnode] = monoiddata.composition(nlazy, lazy[lnode])
      lnode <<= 1
      keydata[lnode] = monoiddata.mapping(nlazy, keydata[lnode])
      keydata[lnode|1] = monoiddata.mapping(nlazy, keydata[lnode|1])
    if rnode:
      lazy[rnode] = monoiddata.composition(nlazy, lazy[rnode])
      rnode <<= 1
      keydata[rnode] = monoiddata.mapping(nlazy, keydata[rnode])
      keydata[rnode|1] = monoiddata.mapping(nlazy, keydata[rnode|1])

  def _update(self, node: int) -> None:
    monoiddata = self.monoiddata
    size, keydata, child = monoiddata.size, monoiddata.keydata, monoiddata.child
    lnode, rnode = child[node<<1], child[node<<1|1]
    size[node] = 1 + size[lnode] + size[rnode]
    keydata[node<<1|1] = monoiddata.op(monoiddata.op(keydata[lnode<<1|1], keydata[node<<1]), keydata[rnode<<1|1])

  def _update_triple(self, x: int, y: int, z: int) -> None:
    monoiddata = self.monoiddata
    size, keydata, child = monoiddata.size, monoiddata.keydata, monoiddata.child
    lx, rx = child[x<<1], child[x<<1|1]
    ly, ry = child[y<<1], child[y<<1|1]
    size[z] = size[x]
    size[x] = 1 + size[lx] + size[rx]
    size[y] = 1 + size[ly] + size[ry]
    keydata[z<<1|1] = keydata[x<<1|1]
    keydata[x<<1|1] = monoiddata.op(monoiddata.op(keydata[lx<<1|1], keydata[x<<1]), keydata[rx<<1|1])
    keydata[y<<1|1] = monoiddata.op(monoiddata.op(keydata[ly<<1|1], keydata[y<<1]), keydata[ry<<1|1])

  def _update_double(self, x: int, y: int) -> None:
    monoiddata = self.monoiddata
    size, keydata, child = monoiddata.size, monoiddata.keydata, monoiddata.child
    lx, rx = child[x<<1], child[x<<1|1]
    size[y] = size[x]
    size[x] = 1 + size[lx] + size[rx]
    keydata[y<<1|1] = keydata[x<<1|1]
    keydata[x<<1|1] = monoiddata.op(monoiddata.op(keydata[lx<<1|1], keydata[x<<1]), keydata[rx<<1|1])

  def _splay(self, path: List[int], d: int) -> None:
    child = self.monoiddata.child
    g = d & 1
    while len(path) > 1:
      pnode = path.pop()
      gnode = path.pop()
      f = d >> 1 & 1
      node = child[pnode<<1|g^1]
      nnode = (pnode if g == f else node) << 1 | f
      child[pnode<<1|g^1] = child[node<<1|g]
      child[node<<1|g] = pnode
      child[gnode<<1|f^1] = child[nnode]
      child[nnode] = gnode
      self._update_triple(gnode, pnode, node)
      if not path:
        return
      d >>= 2
      g = d & 1
      child[path[-1]<<1|g^1] = node
    pnode = path.pop()
    node = child[pnode<<1|g^1]
    child[pnode<<1|g^1] = child[node<<1|g]
    child[node<<1|g] = pnode
    self._update_double(pnode, node)

  def _kth_elm_splay(self, node: int, k: int) -> int:
    size, child = self.monoiddata.size, self.monoiddata.child
    if k < 0: k += size[node]
    d = 0
    path = []
    while True:
      self._propagate(node)
      t = size[child[node<<1]]
      if t == k:
        if path:
          self._splay(path, d)
        return node
      d = d << 1 | (t > k)
      path.append(node)
      node = child[node<<1|(t<k)]
      if t < k:
        k -= t + 1

  def _left_splay(self, node: int) -> int:
    if not node: return 0
    self._propagate(node)
    child = self.monoiddata.child
    if not child[node<<1]: return node
    path = []
    while child[node<<1]:
      path.append(node)
      node = child[node<<1]
      self._propagate(node)
    self._splay(path, (1<<len(path))-1)
    return node

  def _right_splay(self, node: int) -> int:
    if not node: return 0
    self._propagate(node)
    child = self.monoiddata.child
    if not child[node<<1|1]: return node
    path = []
    while child[node<<1|1]:
      path.append(node)
      node = child[node<<1|1]
      self._propagate(node)
    self._splay(path, 0)
    return node

  def reserve(self, n: int) -> None:
    self.monoiddata.reserve(n)

  def merge(self, other: 'LazySplayTree') -> None:
    assert self.monoiddata is other.monoiddata
    if not other.node: return
    if not self.node:
      self.node = other.node
      return
    self.node = self._right_splay(self.node)
    self.monoiddata.child[self.node<<1|1] = other.node
    self._update(self.node)

  def split(self, k: int) -> Tuple['LazySplayTree', 'LazySplayTree']:
    assert -len(self) < k <= len(self), \
        f'IndexError: LazySplayTree.split({k}), len={len(self)}'
    if k < 0: k += len(self)
    if k >= self.monoiddata.size[self.node]:
      return self, LazySplayTree(monoiddata=self.monoiddata, _node=0)
    self.node = self._kth_elm_splay(self.node, k)
    left = LazySplayTree(monoiddata=self.monoiddata, _node=self.monoiddata.child[self.node<<1])
    self.monoiddata.child[self.node<<1] = 0
    self._update(self.node)
    return left, self

  def _internal_split(self, k: int) -> Tuple[int, int]:
    if k >= self.monoiddata.size[self.node]:
      return self.node, 0
    self.node = self._kth_elm_splay(self.node, k)
    left = self.monoiddata.child[self.node<<1]
    self.monoiddata.child[self.node<<1] = 0
    self._update(self.node)
    return left, self.node

  def reverse(self, l: int, r: int) -> None:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.reverse({l}, {r}), len={len(self)}'
    if l == r: return
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    if l:
      left = self._kth_elm_splay(left, l-1)
    monoiddata.rev[monoiddata.child[left<<1|1] if l else left] ^= 1
    if right:
      monoiddata.child[right<<1] = left
      self._update(right)
      self.node = right
    else:
      self.node = left

  def all_reverse(self) -> None:
    self.monoiddata.rev[self.node] ^= 1

  def apply(self, l: int, r: int, f: F) -> None:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.apply({l}, {r}), len={len(self)}'
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    keydata, lazy = monoiddata.keydata, monoiddata.lazy
    if l:
      left = self._kth_elm_splay(left, l-1)
    node = monoiddata.child[left<<1|1] if l else left
    keydata[node<<1] = monoiddata.mapping(f, keydata[node<<1])
    keydata[node<<1|1] = monoiddata.mapping(f, keydata[node<<1|1])
    lazy[node] = monoiddata.composition(f, lazy[node])
    if l:
      self._update(left)
    if right:
      monoiddata.child[right<<1] = left
      self._update(right)
      self.node = right
    else:
      self.node = left

  def all_apply(self, f: F) -> None:
    if not self.node: return
    monoiddata, node = self.monoiddata, self.node
    monoiddata.keydata[node<<1] = monoiddata.mapping(f, monoiddata.keydata[node<<1])
    monoiddata.keydata[node<<1|1] = monoiddata.mapping(f, monoiddata.keydata[node<<1|1])
    monoiddata.lazy[node] = monoiddata.composition(f, monoiddata.lazy[node])

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.prod({l}, {r}), len={len(self)}'
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    if l:
      left = self._kth_elm_splay(left, l-1)
    res = monoiddata.keydata[(monoiddata.child[left<<1|1] if l else left)<<1|1]
    if right:
      monoiddata.child[right<<1] = left
      self._update(right)
      self.node = right
    else:
      self.node = left
    return res

  def all_prod(self) -> T:
    return self.monoiddata.keydata[self.node<<1|1]

  def insert(self, k: int, key: T) -> None:
    assert -len(self) <= k <= len(self), \
        f'IndexError: LazySplayTree.insert({k}, {key}), len={len(self)}'
    if k < 0: k += len(self)
    monoiddata = self.monoiddata
    node = self._make_node(key)
    if not self.node:
      self.node = node
      return
    child = monoiddata.child
    if k >= monoiddata.size[self.node]:
      child[node<<1] = self._right_splay(self.node)
    else:
      self.node = self._kth_elm_splay(self.node, k)
      if child[self.node<<1]:
        child[node<<1] = child[self.node<<1]
        child[self.node<<1] = 0
        self._update(self.node)
      child[node<<1|1] = self.node
    self._update(node)
    self.node = node

  def append(self, key: T) -> None:
    monoiddata = self.monoiddata
    node = self._right_splay(self.node)
    self.node = self._make_node(key)
    monoiddata.child[self.node<<1] = node
    self._update(self.node)

  def appendleft(self, key: T) -> None:
    node = self._left_splay(self.node)
    self.node = self._make_node(key)
    self.monoiddata.child[self.node<<1|1] = node
    self._update(self.node)

  def pop(self, k: int=-1) -> T:
    assert -len(self) <= k < len(self), \
        f'IndexError: LazySplayTree.pop({k})'
    monoiddata = self.monoiddata
    if k == -1:
      node = self._right_splay(self.node)
      self._propagate(node)
      self.node = monoiddata.child[node<<1]
      return monoiddata.keydata[node<<1]
    self.node = self._kth_elm_splay(self.node, k)
    res = monoiddata.keydata[self.node<<1]
    if not monoiddata.child[self.node<<1]:
      self.node = monoiddata.child[self.node<<1|1]
    elif not monoiddata.child[self.node<<1|1]:
      self.node = monoiddata.child[self.node<<1]
    else:
      node = self._right_splay(monoiddata.child[self.node<<1])
      monoiddata.child[node<<1|1] = monoiddata.child[self.node<<1|1]
      self.node = node
      self._update(self.node)
    return res

  def popleft(self) -> T:
    assert self, f'IndexError: LazySplayTree.popleft()'
    node = self._left_splay(self.node)
    self.node = self.monoiddata.child[node<<1|1]
    return self.monoiddata.keydata[node<<1]

  def rotate(self, x: int) -> None:
    # 「末尾をを削除し先頭に挿入」をx回
    n = self.monoiddata.size[self.node]
    l, self = self.split(n-(x%n))
    self.merge(l)

  def tolist(self) -> List[T]:
    node = self.node
    child, keydata = self.monoiddata.child, self.monoiddata.keydata
    stack = newlist_hint(len(self))
    result = newlist_hint(len(self))
    while stack or node:
      if node:
        self._propagate(node)
        stack.append(node)
        node = child[node<<1]
      else:
        node = stack.pop()
        result.append(keydata[node<<1])
        node = child[node<<1|1]
    return result

  def clear(self) -> None:
    self.node = 0

  def __setitem__(self, k: int, key: T):
    assert -len(self) <= k < len(self), f'IndexError: LazyAVLTree.__setitem__({k})'
    self.node = self._kth_elm_splay(self.node, k)
    self.monoiddata.keydata[self.node<<1] = key
    self._update(self.node)

  def __getitem__(self, k: int) -> T:
    assert -len(self) <= k < len(self), f'IndexError: LazyAVLTree.__getitem__({k})'
    self.node = self._kth_elm_splay(self.node, k)
    return self.monoiddata.keydata[self.node<<1]

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.monoiddata.size[self.node]:
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return self.monoiddata.size[self.node]

  def __str__(self):
    return str(self.tolist())

  def __bool__(self):
    return self.node != 0

  def __repr__(self):
    return f'LazySplayTree({self.tolist()})'

def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None
id = None

