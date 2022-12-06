# https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeMultiSet2.py


import sys
from typing import Union, Generic, Iterable, List, TypeVar, Tuple
T = TypeVar("T")


class Node:

  def __init__(self, key, val) -> None:
    self.key = key
    self.val = val
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val}\n'
    return f'key:{self.key, self.val},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeMultiSet2(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    self._len = 0
    self._len_elm = 0
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int):
      mid = (l + r) >> 1
      node = Node(a[mid][0], a[mid][1])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    a = sorted(a)
    self._len = len(a)
    a = self._rle(a)
    self._len_elm = len(a)
    self.node = sort(0, len(a))

  def _rle(self, a: list) -> list:
    now = a[0]
    ret = [[now, 1]]
    for i in a[1:]:
      if i == now:
        ret[-1][1] += 1
        continue
      ret.append([i, 1])
      now = i
    return ret

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
      if not path:
        return tmp
      di >>= 2
      if di & 1 == 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1 == 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
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

  def add(self, key: T, val: int=1) -> None:
    self._len += val
    if self.node is None:
      self._len_elm += 1
      self.node = Node(key, val)
      return
    self._set_search_splay(key)
    if self.node.key == key:
      self.node.val += val
      return
    self._len_elm += 1
    node = Node(key, val)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
    self.node = node
    return

  def discard(self, key: T, val: int=1) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.val > val:
      self.node.val -= val
      self._len -= val
      return True
    self._len -= self.node.val
    self._len_elm -= 1
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
    return True

  def discard_all(self, key: T) -> bool:
    return self.discar(key, self.count(key))

  def count(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    return self.node.val if self.node.key == key else 0

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while True:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        res = node.key
        if node.right is None:
          break
        path.append(node)
        di <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
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
        res = node.key
        if node.right is None:
          break
        path.append(node)
        di <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while True:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        res = node.key
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
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while True:
      if node.key == key:
        break
      elif key < node.key:
        res = node.key
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
    return res

  def pop(self) -> T:
    self.node = self._get_max_splay(self.node)
    res = self.node.key
    self.discard(res)
    return res

  def popleft(self) -> T:
    self.node = self._get_min_splay(self.node)
    res = self.node.key
    self.discard(res)
    return res

  def get_min(self) -> T:
    node = self._get_min_splay(self.node)
    return self.node
 
  def get_max(self) -> T:
    node = self._get_max_splay(self.node)
    return self.node

  def to_l(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self._len_elm():
      sys.setrecursionlimit(self._len_elm()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.extend([node.key]*node.val)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def to_l_items(self) -> List[Tuple[T, int]]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self._len_elm():
      sys.setrecursionlimit(self._len_elm()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def len_elm(self) -> int:
    return self._len_elm

  def clear(self) -> None:
    self.node = None

  def __contains__(self, key: T) -> bool:
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'SplayTreeMultiSet2 ' + str(self)

