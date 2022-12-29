import sys
from typing import Callable, Generic, Tuple, TypeVar, Union, List, Iterable
T = TypeVar("T")


class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.data = key
    self.size = 1
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.data, self.size}\n'
    return f'key:{self.key, self.data, self.size},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeOp(Generic[T]):

  def __init__(self, a: Iterable[T]=[], op: Callable[[T, T], T]=lambda x,y: None, e: T=None, node :Union[Node, None]=None) -> None:
    self.node = node
    self.op = op
    self.e = e
    if a:
      self._build(list(a))
 
  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      self._update(node)
      return node
    self.node = sort(0, len(a))

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.data = node.key
      else:
        node.size = 1 + node.right.size
        node.data = self.op(node.key, node.right.data)
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.data = self.op(node.left.data, node.key)
      else:
        node.size = 1 + node.left.size + node.right.size
        node.data = self.op(self.op(node.left.data, node.key), node.right.data)

  def _splay(self, path: List[Node], di: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if di&1 == di>>1&1:
        if di & 1:
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          pnode.left = node.right
          node.right = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
      else:
        if di & 1:
          tmp = node.left
          node.left = tmp.right
          pnode.right = tmp.left
          tmp.right = node
          tmp.left = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          pnode.left = tmp.right
          tmp.left = node
          tmp.right = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      di >>= 2
      if di & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
    self._update(gnode)
    self._update(node)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0: k += self.__len__()
    di = 0
    node = self.node
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        k -= t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  def merge(self, other: "SplayTreeOp") -> None:
    if self.node is None:
      self.node = other.node
      return
    if other.node is None:
      return
    self.node = self._get_max_splay(self.node)
    self.node.right = other.node
    self._update(self.node)

  def split(self, p: int) -> Tuple["SplayTreeOp", "SplayTreeOp"]:
    if p >= self.__len__():
      return self, SplayTreeOp(op=self.op, e=self.e)
    self._set_kth_elm_splay(p)
    left = SplayTreeOp(node=self.node.left, op=self.op, e=self.e)
    self.node.left, right = None, self
    self._update(right.node)
    return left, right

  def prod(self, l: int, r: int) -> T:
    if l >= r:
      return self.e
    left, right = self.split(r)
    if l == 0:
      res = left.node.data
    else:
      left._set_kth_elm_splay(l-1)
      res = left.node.right.data
    if right.node is None:
      right.node = left.node
    else:
      right.node.left = left.node
      self._update(right.node)
    self.node = right.node
    return res

  def all_prod(self) -> T:
    return self.e if self.node is None else self.node.data

  def insert(self, k: int, key: T) -> None:
    node = Node(key)
    if self.node is None:
      self.node = node
      return
    if k >= self.__len__():
      self._set_kth_elm_splay(self.__len__()-1)
      node.left = self.node
      self.node = node
    else:
      self._set_kth_elm_splay(k)
      if self.node.left is not None:
        node.left = self.node.left
        self.node.left = None
        self._update(self.node)
      node.right = self.node
      self.node = node
    self._update(self.node)

  def append(self, key: T) -> None:
    node = self._get_max_splay(self.node)
    self.node = Node(key)
    self.node.left = node
    self._update(self.node)

  def appendleft(self, key: T) -> None:
    node = self._get_min_splay(self.node)
    self.node = Node(key)
    self.node.right = node
    self._update(self.node)

  def pop(self, k: int =-1) -> T:
    if k == -1:
      node = self._get_max_splay(self.node)
      self.node = node.left
      return node.key
    self._set_kth_elm_splay(k)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_max_splay(self.node.left)
      node.right, self.node = self.node.right, node
    self._update(self.node)
    return res

  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    return node.key

  def copy(self) -> "SplayTreeOp":
    return SplayTreeOp(self.to_l(), op=self.op, e=self.e)

  def clear(self) -> None:
    self.node = None

  def to_l(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self.node.size:
      sys.setrecursionlimit(self.node.size+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def __setitem__(self, k: int, key: T):
    self._set_kth_elm_splay(k)
    self.node.key = key
    self._update(self.node)

  def __getitem__(self, k: int) -> T:
    self._set_kth_elm_splay(k)
    return self.node.key

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __str__(self):
    return '[' + ', '.join(map(str, self.to_l())) + ']'

  def __bool__(self):
    return self.node is not None

  def __repr__(self):
    return 'SplayTreeOp' + str(self)


def op(s, t):
  return

e = 0

