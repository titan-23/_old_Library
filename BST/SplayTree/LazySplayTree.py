# https://github.com/titanium-22/Library/blob/main/BST/SplayTree/LazySplayTree.py


import sys

class Node:

  def __init__(self, key):
    self.key = key
    self.data = key
    self.size = 1
    self.left = None
    self.right = None
    self.lazy = None
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
      self.node = self._build(list(_a))
 
  def _build(self, a: list) -> None:
    def sort(l, r):
      if l >= r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left, node.right = sort(l, mid), sort(mid+1, r)
      self._update(node)
      return node
    return sort(0, len(a))

  def _propagate(self, node) -> None:
    if node is None: return
    if node.rev:
      node.left, node.right = node.right, node.left
      if node.left is not None:
        node.left.rev ^= 1
      if node.right is not None:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy is not None:
      if node.left is not None:
        node.left.data = self.mapping(node.lazy, node.left.data)
        node.left.key = self.mapping(node.lazy, node.left.key)  
        if node.left.lazy is None:
          node.left.lazy = node.lazy
        else:
          node.left.lazy = self.composition(node.lazy, node.left.lazy)
      if node.right is not None:
        node.right.data = self.mapping(node.lazy, node.right.data)
        node.right.key = self.mapping(node.lazy, node.right.key)
        if node.right.lazy is None:
          node.right.lazy = node.lazy
        else:
          node.right.lazy = self.composition(node.lazy, node.right.lazy)
      node.lazy = None

  def _update(self, node) -> None:
    if node is None: return
    node.size, node.data = 1, node.key
    if node.left is not None:
      node.size += node.left.size
      node.data = self.op(node.left.data, node.data)
    if node.right is not None:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)

  def _splay(self, path, di) -> Node:
    # assert len(path) > 0
    while len(path) > 1:
      node, pnode = path.pop(), path.pop()
      ndi, pdi = di&1, di>>1&1
      di >>= 2
      if ndi == pdi:
        if ndi:
          tmp, node.left = node.left, node.left.right
          tmp.right, pnode.left, node.right = node, node.right, pnode
        else:
          tmp, node.right = node.right, node.right.left
          tmp.left, pnode.right, node.left = node, node.left, pnode
      else:
        if ndi:
          tmp, node.left = node.left, node.left.right
          pnode.right, tmp.right, tmp.left = tmp.left, node, pnode
        else:
          tmp, node.right = node.right, node.right.left
          pnode.left, tmp.left, tmp.right = tmp.right, node, pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      if di & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1:
      node = gnode.left
      gnode.left, node.right = node.right, gnode
      self._update(node.right)
    else:
      node = gnode.right
      gnode.right, node.left = node.left, gnode
      self._update(node.left)
    self._update(node)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    now, di = 0, 0
    node, path = self.node, []
    while node is not None:
      self._propagate(node)
      t = now if node.left is None else now + node.left.size
      if t == k:
        if len(path) > 0:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di, node = di<<1|1, node.left
      else:
        path.append(node)
        di, node, now = di<<1, node.right, t+1
    raise IndexError

  def _get_min_splay(self, node) -> Node:
    self._propagate(node)
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
      self._propagate(node)
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node) -> Node:
    self._propagate(node)
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
      self._propagate(node)
    return self._splay(path, 0)

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
    left = LazySplayTree([], self.op, self.mapping, self.composition, node=self.node.left)
    self.node.left, right = None, self
    self._update(right.node)
    return left, right

  def reverse(self, l: int, r: int):
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
    # assert l < r
    left, right = self.split(r)
    if l == 0:
      left.node.key = self.mapping(f, left.node.key)
      left.node.data = self.mapping(f, left.node.data)
      if left.node.lazy is None:
        left.node.lazy = f
      else:
        left.node.lazy = self.composition(f, left.node.lazy)
    else:
      left._set_kth_elm_splay(l-1)
      left.node.right.key = self.mapping(f, left.node.right.key)
      left.node.right.data = self.mapping(f, left.node.right.data)
      if left.node.right.lazy is None:
        left.node.right.lazy = f
      else:
        left.node.right.lazy = self.composition(f, left.node.right.lazy)
      self._update(left.node)
    if right.node is None:
      right.node = left.node
    else:
      right.node.left = left.node
      self._update(right.node)
    self.node = right.node

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
    assert self.node is not None
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
      if indx < 0:
        indx += self.__len__()
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
    if indx < 0:
      indx += self.__len__()
    self._set_kth_elm_splay(indx)
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

  def copy(self):
    return LazySplayTree(self, self.op, self.mapping, self.composition)

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

  def __setitem__(self, indx: int, key):
    self._set_kth_elm_splay(indx)
    self.node.key = key
    # self._propagate(self.node)
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
    return '[' + ', '.join(map(str, self)) + ']'

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


