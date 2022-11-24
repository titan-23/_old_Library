# https://github.com/titanium-22/Library/blob/main/BST/SplayTree/LazySplayTree.py


import sys
from typing import List


class Node:

  def __init__(self, key):
    self.key = key
    self.data = key
    self.lazy = None
    self.left = None
    self.right = None
    self.size = 1
    self.rev = 0

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.data, self.lazy, self.rev, self.size}\n'
    return f'key:{self.key, self.data, self.lazy, self.rev, self.size},\n left:{self.left},\n right:{self.right}\n'


class LazySplayTree:

  def __init__(self, _a=[], op=lambda x,y:None, mapping=None, composition=None, node=None) -> None:
    self.node = node
    self.op = op
    self.mapping = mapping
    self.composition = composition
    if _a:
      self._build(list(_a))
 
  def _build(self, a: list) -> None:
    def sort(l: int, r: int):
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      self._update(node)
      return node
    self.node = sort(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node.rev:
      node.left, node.right = node.right, node.left
      if node.left is not None:
        node.left.rev ^= 1
      if node.right is not None:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy is not None:
      lazy = node.lazy
      if node.left is not None:
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = lazy if node.left.lazy is None else self.composition(lazy, node.left.lazy)
      if node.right is not None:
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.lazy = lazy if node.right.lazy is None else self.composition(lazy, node.right.lazy)
      node.lazy = None

  def _update(self, node: Node) -> None:
    if node.left is None:
      node.size = 1
      node.data = node.key
    else:
      node.size = 1 + node.left.size
      node.data = self.op(node.left.data, node.key)
    if node.right is not None:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)

  def _splay(self, path: List[Node], di: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if di&1 == di>>1&1:
        if di&1 == 1:
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
        if di&1 == 1:
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
      self._update(node.right)
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self._update(node.left)
    self._update(node)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    # assert 0 <= k < self.__len__()
    now = 0
    di = 0
    node = self.node
    path = []
    while True:
      self._propagate(node)
      t = now if node.left is None else now + node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di = di<<1|1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        now = t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None: return None
    self._propagate(node)
    if node.left is None: return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
      self._propagate(node)
    # return self._splay(path, (1<<len(path))-1)
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      tmp = node.left
      node.left = tmp.right
      tmp.right = node
      pnode.left = node.right
      node.right = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      path[-1].left = tmp
    gnode = path[0]
    node = gnode.left
    gnode.left = node.right
    node.right = gnode
    self._update(node.right)
    self._update(node)
    return node

  def _get_max_splay(self, node: Node) -> Node:
    if node is None: return None
    self._propagate(node)
    if node.right is None: return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
      self._propagate(node)
    # return self._splay(path, 0)
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      tmp = node.right
      node.right = tmp.left
      tmp.left = node
      pnode.right = node.left
      node.left = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      path[-1].right = tmp
    gnode = path[0]
    node = gnode.right
    gnode.right = node.left
    node.left = gnode
    self._update(node.left)
    self._update(node)
    return node

  def merge(self, other) -> None:
    if self.node is None:
      self.node = other.node
      return
    if other.node is None:
      return
    self.node = self._get_max_splay(self.node)
    self.node.right = other.node
    self._update(self.node)

  def split(self, indx) -> tuple:
    if indx >= self.__len__():
      return self, LazySplayTree([], self.op, self.mapping, self.composition)
    self._set_kth_elm_splay(indx)
    left = LazySplayTree([], self.op, self.mapping, self.composition, self.node.left)
    self.node.left, right = None, self
    self._update(right.node)
    return left, right

  def reverse(self, l: int, r: int):
    if l >= r: return
    left, right = self.split(r)
    if l == 0:
      left.node.rev ^= 1
    else:
      left._set_kth_elm_splay(l-1)
      left.node.right.rev ^= 1
    if right.node is None:
      right.node = left.node
    else:
      right.node.left = left.node
      self._update(right.node)
    self.node = right.node

  def apply(self, l: int, r: int, f):
    if l >= r: return
    left, right = self.split(r)
    if l == 0:
      left.node.key = self.mapping(f, left.node.key)
      left.node.data = self.mapping(f, left.node.data)
      left.node.lazy = f if left.node.lazy is None else self.composition(f, left.node.lazy)
    else:
      left._set_kth_elm_splay(l-1)
      node = left.node.right
      node.key = self.mapping(f, node.key)
      node.data = self.mapping(f, node.data)
      node.lazy = f if node.lazy is None else self.composition(f, node.lazy)
      self._update(left.node)
    if right.node is None:
      right.node = left.node
    else:
      right.node.left = left.node
      self._update(right.node)
    self.node = right.node

  def all_apply(self, f):
    self.node.key = self.mapping(f, self.node.key)
    self.node.data = self.mapping(f, self.node.data)
    self.node.lazy = f if self.node.lazy is None else self.composition(f, self.node.lazy)

  def prod(self, l: int, r: int):
    # assert l < r
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

  def all_prod(self):
    return self.node.data

  def insert(self, indx: int, key):
    node = Node(key)
    if self.node is None:
      self.node = node
      return
    if indx >= self.__len__():
      self._set_kth_elm_splay(self.__len__()-1)
      node.left = self.node
      self.node = node
    else:
      self._set_kth_elm_splay(indx)
      if self.node.left is not None:
        node.left = self.node.left
        self.node.left = None
        self._update(self.node)
      node.right = self.node
      self.node = node
    self._update(self.node)

  def append(self, key):
    node = self._get_max_splay(self.node)
    self.node = Node(key)
    self.node.left = node
    self._update(self.node)

  def appendleft(self, key):
    node = self._get_min_splay(self.node)
    self.node = Node(key)
    self.node.right = node
    self._update(self.node)

  def popleft(self):
    node = self._get_min_splay(self.node)
    self._propagate(node)
    self.node = node.right
    return node.key

  def pop(self, indx: int =-1):
    if indx == -1:
      node = self._get_max_splay(self.node)
      self._propagate(node)
      self.node = node.left
      return node.key
    self._set_kth_elm_splay(indx)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_max_splay(self.node.left)
      node.right = self.node.right
      self.node = node
      self._update(self.node)
    return res

  def copy(self):
    a = self.to_l()
    return LazySplayTree(a, self.op, self.mapping, self.composition)

  def show(self, sep=' '):
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      print(node.key, end=sep)
      if node.right is not None:
        rec(node.right)
    if self.node is not None:
      rec(self.node)

  def to_l(self):
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    a = []
    if self.node is not None:
      rec(self.node)
    return a

  def __setitem__(self, indx: int, key):
    self._set_kth_elm_splay(indx)
    self.node.key = key
    self._update(self.node)

  def __getitem__(self, item):
    if type(item) is int:
      self._set_kth_elm_splay(item)
      return self.node.key
    elif type(item) is slice:
      s = self.copy()
      if item.step is not None:
        s = LazySplayTree(list(s)[item], self.op, self.mapping, self.composition)
      else:
        start = item.start if item.start is not None else 0
        stop  = item.stop if item.stop is not None else s.__len__()
        left, right = s.split(stop)
        lleft, s = left.split(start)
      return s
    raise KeyError

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
    return 'LazySplayTree ' + str(self)


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

