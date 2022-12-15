# https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py


import sys
from typing import Union, Generic, Iterable, List, TypeVar
T = TypeVar("T")


class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.size = 1
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size}\n'
    return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeSet(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
      return node
    a = list(a)
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      aa = sorted(a)
      a = [aa[0]]
      for i in range(1, len(aa)):
        if aa[i] != a[-1]:
          a.append(aa[i])
    self.node = sort(0, len(a))

  def _update(self, node: Node) -> None:
    node.size = 1 + (0 if node.left is None else node.left.size) + (0 if node.right is None else node.right.size)

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
          self._update(pnode)
          node.size = 1 + (0 if node.left is None else node.left.size) + pnode.size
          tmp.size = 1 + (0 if tmp.left is None else tmp.left.size) + node.size
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
          self._update(pnode)
          node.size = 1 + pnode.size + (0 if node.right is None else node.right.size)
          tmp.size = 1 + node.size + (0 if tmp.right is None else tmp.right.size)
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
        tmp.size = 1 + node.size + pnode.size
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
      self._update(gnode)
      node.size = 1 + (0 if node.left is None else node.left.size) + gnode.size
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self._update(gnode)
      node.size = 1 + gnode.size + (0 if node.right is None else node.right.size)
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key:
      return
    path = []
    di = 0
    while True:
      if node.key == key:
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        di <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, di)

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    assert 0 <= k < self.__len__()
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

  def add(self, key: T) -> bool:
    if self.node is None:
      self.node = Node(key)
      return True
    self._set_search_splay(key)
    if self.node.key == key:
      return False
    node = Node(key)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
      self._update(node.right)
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
      self._update(node.left)
    self._update(node)
    self.node = node
    return True

  def discard(self, key: T) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self._update(node.left)
      self.node = node
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key < key:
      res += 1
    return res

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key <= key:
      res += 1
    return res

  def pop(self, k: int=-1) -> T:
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
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self._update(node)
      self.node = node
    return res

  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    return node.key

  def clear(self) -> None:
    self.node = None

  def to_l(self) -> List[T]:
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

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __getitem__(self, k) -> T:
    self._set_kth_elm_splay(k)
    return self.node.key

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'SplayTreeSet ' + str(self)


