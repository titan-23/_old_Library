import sys
from typing import Union, Generic, Iterable, List, TypeVar
T = TypeVar("T")


class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key}\n'
    return f'key:{self.key},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeSetTopDown(Generic[T]):

  _NIL = Node(None)

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    self.len = 0
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    a = sorted(set(a))
    self.len = len(a)
    self.node = sort(0, len(a))

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key: return
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while True:
      if node.key == key: break
      if key < node.key:
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[None, T]:
    node = self.node
    if node is None: return None
    if node.key == key: return key
    ge = None
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while True:
      if node.key == key:
        ge = key
        break
      if key < node.key:
        ge = node.key
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          ge = node.key
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node
    return ge

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[None, T]:
    gt = None
    node = self.node
    if node is None: return gt
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while True:
      if key < node.key:
        gt = node.key
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          gt = node.key
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node
    return gt

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[None, T]:
    node = self.node
    if node is None: return None
    if node.key == key: return key
    le = None
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while True:
      if node.key == key:
        le = key
        break
      if key < node.key:
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        le = node.key
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          le = node.key
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node
    return le

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[None, T]:
    lt = None
    node = self.node
    if node is None: return lt
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while True:
      if key <= node.key:
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        lt = node.key
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          lt = node.key
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node
    return lt

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None: return node
    par = SplayTreeSetTopDown._NIL
    left = par
    right = par
    while node.left is not None:
      new = node.left
      node.left = new.right
      new.right = node
      node = new
      if node.left is None: break
      right.left = node
      right = node
      node = node.left
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    return node

  def add(self, key: T) -> bool:
    if self.node is None:
      self.node = Node(key)
      self.len += 1
      return True
    self._set_search_splay(key)
    if self.node.key == key:
      return False
    node = Node(key)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
    self.node = node
    self.len += 1
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
      self.node = node
    self.len -= 1
    return True

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

  def get_min(self) -> T:
    self.node = self._get_max_splay(self.node)
    return self.node.key

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'SplayTreeSetTopDown' + str(self)

