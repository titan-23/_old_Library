import sys
from typing import Union, Generic, Iterable, List, TypeVar
T = TypeVar("T")


class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.par = None
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'(key):{self.key}\n'
    return f'(key,par):{self.key, self.par.key},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeSet2(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    self.len = 0
    a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
        node.left.par = node
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.right.par = node
      return node
    # if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
    #   aa = sorted(a)
    #   a = [aa[0]]
    #   for i in range(1, len(aa)):
    #     if aa[i] != a[-1]:
    #       a.append(aa[i])
    self.len = len(a)
    self.node = sort(0, len(a))

  def _splay(self, node: Node) -> Node:
    if node is None or node.par is None: return node
    while node.par.par is not None:
      pnode = node.par
      gnode = pnode.par
      node.par = gnode.par
      if (pnode.key < gnode.key) == (node.key < pnode.key):
        if node.key < pnode.key:
          tmp = node.right
          pnode.left = tmp
          if tmp:
            tmp.par = pnode
          node.right = pnode
          pnode.par = node
          tmp = pnode.right
          gnode.left = tmp
          if tmp:
            tmp.par = gnode
          pnode.right = gnode
          gnode.par = pnode
        else:
          tmp = node.left
          pnode.right = node.left
          if tmp:
            tmp.par = pnode
          node.left = pnode
          pnode.par = node
          tmp = pnode.left
          gnode.right = tmp
          if tmp:
            tmp.par = gnode
          pnode.left = gnode
          gnode.par = pnode
      else:
        if node.key < pnode.key:
          tmp = node.right
          pnode.left = tmp
          if tmp:
            tmp.par = pnode
          node.right = pnode
          pnode.par = node
          tmp = node.left
          gnode.right = tmp
          if tmp:
            tmp.par = gnode
          node.left = gnode
          gnode.par = node
        else:
          tmp = node.left
          pnode.right = tmp
          if tmp:
            tmp.par = pnode
          node.left = pnode
          pnode.par = node
          tmp = node.right
          gnode.left = tmp
          if tmp:
            tmp.par = gnode
          node.right = gnode
          gnode.par = node
      if node.par is None:
        return node
      if node.key < node.par.key:
        node.par.left = node
      else:
        node.par.right = node
    gnode = node.par
    node.par = None
    if node.key < gnode.key:
      gnode.left = node.right
      if gnode.left: gnode.left.par = gnode
      node.right = gnode
      gnode.par = node
    else:
      gnode.right = node.left
      if gnode.right: gnode.right.par = gnode
      node.left = gnode
      gnode.par = node
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key: return
    while True:
      if node.key == key:
        break
      elif key < node.key:
        if node.left is None:
          break
        node = node.left
      else:
        if node.right is None:
          break
        node = node.right
    self.node = self._splay(node)

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    while node.left:
      node = node.left
    return self._splay(node)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    while node.right is not None:
      node = node.right
    return self._splay(node)

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
      if node.left: node.left.par = node
      node.right = self.node
      if node.right: node.right.par = node
      self.node.left = None
    else:
      node.left = self.node
      if node.left: node.left.par = node
      node.right = self.node.right
      if node.right: node.right.par = node
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
      node.left.par = node
      self.node = node
    self.node.par = None
    self.len -= 1
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    res = None
    snode = None
    while node is not None:
      snode = node
      if node.key == key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    self.node = self._splay(snode)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    res = None
    snode = None
    while node is not None:
      snode = node
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    self.node = self._splay(snode)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    res = None
    snode = None
    while node is not None:
      snode = node
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    self.node = self._splay(snode)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    res = None
    snode = None
    while node is not None:
      snode = node
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    self.node = self._splay(snode)
    return res

  def pop(self) -> T:
    node = self._get_max_splay(self.node)
    self.node = node.left
    self.node.par = None
    self.len -= 1
    return node.key

  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    self.node.par = None
    self.len -= 1
    return node.key

  def get_min(self) -> T:
    self.node = self._get_min_splay(self.node)
    return self.node.key
 
  def get_max(self) -> T:
    self.node = self._get_max_splay(self.node)
    return self.node.key

  def clear(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
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

  def __getitem__(self, k):  # 先頭と末尾しか対応していない
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'SplayTreeSet2(' + str(self) + ')'


#  -----------------------  #

import sys
input = lambda: sys.stdin.readline().rstrip()

n, q = map(int, input().split())
s = input()
st = SplayTreeSet2(i for i, c in enumerate(s) if c == '1')

for _ in range(q):
  c, k = map(int, input().split())
  if c == 0:
    st.add(k)
  elif c == 1:
    st.discard(k)
  elif c == 2:
    print(1 if k in st else 0)
  elif c == 3:
    res = st.ge(k)
    print(-1 if res is None else res)
  else:
    res = st.le(k)
    print(-1 if res is None else res)
