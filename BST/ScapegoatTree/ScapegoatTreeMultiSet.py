# https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeMultiSet.py


import math
from typing import Union, List, TypeVar, Generic, Iterable, Tuple
T = TypeVar("T")


class Node:
  
  def __init__(self, key, val: int):
    self.key = key
    self.val = val
    self.left = None
    self.right = None
    self.size = 1
    self.valsize = val

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val, self.size, self.valsize}\n'
    return f'key:{self.key, self.val, self.size, self.valsize},\n left:{self.left},\n right:{self.right}\n'


class ScapegoatTreeMultiSet(Generic[T]):
 
  alpha = 0.75
  beta = math.log2(1/alpha)
 
  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    if a:
      self._build(a)

  def _rle(self, li: List[T]) -> List[Tuple[T, int]]:
    now = li[0]
    ret = [[now, 1]]
    for i in li[1:]:
      if i == now:
        ret[-1][1] += 1
        continue
      ret.append([i, 1])
      now = i
    return ret
 
  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid][0], a[mid][1])
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
        node.valsize += node.left.valsize
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
        node.valsize += node.right.valsize
      return node
    a = self._rle(sorted(a))
    self.node = sort(0, len(a))
 
  def _rebuild(self, node: Node) -> Node:
    def get(node: Node) -> None:
      if node.left is not None:
        get(node.left)
      a.append(node)
      if node.right is not None:
        get(node.right)
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = a[mid]
      node.size = 1
      node.valsize = node.val
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
        node.valsize += node.left.valsize
      else:
        node.left = None
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
        node.valsize += node.right.valsize
      else:
        node.right = None
      return node
    a = []
    get(node)
    return sort(0, len(a))
 
  def _kth_elm(self, k: int) -> Tuple[T, int]:
    if k < 0:
      k += self.__len__()
    # assert 0 <= k < self.__len__()
    node = self.node
    while True:
      t = node.val if node.left is None else node.val + node.left.valsize
      if t-node.val <= k and k < t:
        return node.key, node.val
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t

  def _kth_elm_tree(self, k: int) -> Tuple[T, int]:
    if k < 0:
      k += self.len_elm()
    # assert 0 <= k < self.len_elm()
    node = self.node
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key, node.val
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def add(self, key, val=1) -> None:
    node = self.node
    if self.node is None:
      self.node = Node(key, val)
      return
    path = []
    while node is not None:
      path.append(node)
      if key == node.key:
        node.val += val
        for p in path:
          p.valsize += val
        return        
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    if key < path[-1].key:
      path[-1].left = Node(key, val)
    else:
      path[-1].right = Node(key, val)
    if len(path)*ScapegoatTreeMultiSet.beta > math.log(self.len_elm()):
      node_size = 1
      while path:
        pnode = path.pop()
        pnode_size = pnode.size + 1
        if ScapegoatTreeMultiSet.alpha * pnode_size < node_size:
          break
        node_size = pnode_size
      new_node = self._rebuild(pnode)
      if not path:
        self.node = new_node
        return
      if new_node.key < path[-1].key:
        path[-1].left = new_node
      else:
        path[-1].right = new_node
    for p in path:
      p.size += 1
      p.valsize += val
    return
 
  def _discard(self, key: T) -> bool:
    path = []
    node = self.node
    di = 1
    cnt = 0
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        node = node.left
        di = 1
      else:
        path.append(node)
        node = node.right
        di = 0
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else 0
      while lmax.right is not None:
        cnt += 1
        path.append(lmax)
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
      return True
    for _ in range(cnt):
      p = path.pop()
      p.size -= 1
      p.valsize -= lmax_val
    for p in path:
      p.size -= 1
      p.valsize -= 1
    return True

  def discard(self, key, val=1) -> bool:
    path = []
    node = self.node
    while node is not None:
      path.append(node)
      if key < node.key:
        node = node.left
      elif key > node.key:
        node = node.right
      else:
        break
    else:
      return False
    if val > node.val:
      val = node.val - 1
      if val > 0:
        node.val -= val
        while path:
          path.pop().valsize -= val
    if node.val == 1:
      self._discard(key)
    else:
      node.val -= val
      while path:
        path.pop().valsize -= val
    return True

  def count(self, key: T) -> int:
    node = self.node
    while node is not None:
      if key == node.key:
        return node.val
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return 0

  def discard_all(self, key: T) -> None:
    self.discard(key, self.count(key))

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        return key
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        return key
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.valsize
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        k += node.val if node.left is None else node.left.valsize + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

  '''Count the number of keys < key. / O(logN)'''
  def index_keys(self, key: T) -> int:
    k = 0
    node = self.node
    while node:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return k

  '''Count the number of keys <= key. / O(logN)'''
  def index_right_keys(self, key: T) -> int:
    k = 0
    node = self.node
    while node:
      if key == node.key:
        k += node.val if node.left is None else node.left.size + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return k

  def pop(self, k=-1) -> T:
    if k < 0:
      k += self.__len__()
    x = self.__getitem__(k)
    self.discard(x)
    return x

  def popleft(self) -> T:
    return self.pop(0)

  def items(self):
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)

  def keys(self):
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)[0]

  def values(self):
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)[1]

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.to_l_items())) + '}')

  def get_elm(self, k: int) -> T:
    return self._kth_elm_tree(k)[0]

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def to_l(self) -> List[T]:
    a = []
    if self.node is None:
      return a
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
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def __contains__(self, key: T):
    node = self.node
    while node is not None:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __getitem__(self, k):
    return self._kth_elm(k)[0]

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self._kth_elm(self.__iter)[0]
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self._kth_elm(-i-1)[0]

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'ScapegoatTreeMultiSet ' + str(self)


