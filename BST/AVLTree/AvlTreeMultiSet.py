# https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AvlTreeMultiSet.py


from typing import Generic, Iterable, Tuple, TypeVar, Union, List
T = TypeVar("T")


class Node:

  def __init__(self, key, val: int):
    self.key = key
    self.val = val
    self.valsize = val
    self.size = 1
    self.left = None
    self.right = None
    self.balance = 0

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val, self.size, self.valsize}\n'
    return f'key:{self.key, self.val, self.size, self.valsize},\n left:{self.left},\n right:{self.right}\n'


class AVLTreeMultiSet(Generic[T]):

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
    def sort(l: int, r: int) -> Tuple[Node, int]:
      mid = (l + r) >> 1
      node = Node(a[mid][0], a[mid][1])
      h = 0
      if l != mid:
        left, hl = sort(l, mid)
        node.left = left
        node.size += left.size
        node.valsize += left.valsize
        node.balance = hl
        h = hl
      if mid+1 != r:
        right, hr = sort(mid+1, r)
        node.right = right
        node.size += right.size
        node.valsize += right.valsize
        node.balance -= hr
        if hr > h:
          h = hr
      return node, h+1
    a = self._rle(sorted(a))
    self.node = sort(0, len(a))[0]

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    u.valsize = node.valsize
    if u.left is None:
      node.size -= 1
      node.valsize -= u.val
    else:
      node.size -= u.left.size + 1
      node.valsize -= u.left.valsize + u.val
    node.left = u.right
    u.right = node
    if u.balance == 1:
      u.balance = 0
      node.balance = 0
    else:
      u.balance = -1
      node.balance = 1
    return u

  def _rotate_R(self, node: Node) -> Node:
    u = node.right
    u.size = node.size
    u.valsize = node.valsize
    if u.right is None:
      node.size -= 1
      node.valsize -= u.val
    else:
      node.size -= u.right.size + 1
      node.valsize -= u.right.valsize + u.val
    node.right = u.left
    u.left = node
    if u.balance == -1:
      u.balance = 0
      node.balance = 0
    else:
      u.balance = 1
      node.balance = -1
    return u

  def _update_balance(self, node: Node) -> None:
    if node.balance == 1:
      node.right.balance = -1
      node.left.balance = 0
    elif node.balance == -1:
      node.right.balance = 0
      node.left.balance = 1
    else:
      node.right.balance = 0
      node.left.balance = 0
    node.balance = 0

  def _rotate_LR(self, node: Node) -> Node:
    B = node.left
    E = B.right
    E.size = node.size
    E.valsize = node.valsize
    if E.right is None:
      node.size -= B.size
      node.valsize -= B.valsize
      B.size -= 1
      B.valsize -= E.val
    else:
      node.size -= B.size - E.right.size
      node.valsize -= B.valsize - E.right.valsize
      B.size -= E.right.size + 1
      B.valsize -= E.right.valsize + E.val
    B.right = E.left
    E.left = B
    node.left = E.right
    E.right = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: Node) -> Node:
    C = node.right
    D = C.left
    D.size = node.size
    D.valsize = node.valsize
    if D.left is None:
      node.size -= C.size
      node.valsize -= C.valsize
      C.size -= 1
      C.valsize -= D.val
    else:
      node.size -= C.size - D.left.size
      node.valsize -= C.valsize - D.left.valsize
      C.size -= D.left.size + 1
      C.valsize -= D.left.valsize + D.val
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def _kth_elm(self, k: int) -> Tuple[T, int]:
    if k < 0:
      k += self.__len__()
    # assert 0 <= k < self.__len__()
    node = self.node
    while True:
      t = node.val if node.left is None else node.val + node.left.valsize
      if t-node.val <= k < t:
        return node.key, node.val
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t

  def _kth_elm_tree(self, k: int) -> Tuple[T, int]:
    if k < 0:
      k += self.len_elm()
    assert 0 <= k < self.len_elm()
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

  def _discard(self, key) -> bool:
    path = []
    di = 0
    fdi = 0
    node = self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right

    if node.left is not None and node.right is not None:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = node.left
      while lmax.right is not None:
        path.append(lmax)
        di <<= 1
        fdi <<= 1
        fdi |= 1
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax

    cnode = node.right if node.left is None else node.left
    if path:
      if di & 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
      return True

    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1 if di & 1 else -1
      pnode.size -= 1
      pnode.valsize -= lmax_val if fdi & 1 else 1
      di >>= 1
      fdi >>= 1

      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance < 0 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance> 0 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break

      if new_node is not None:
        if not path:
          self.node = new_node
          return    
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
        if new_node.balance != 0:
          break

    while path:
      pnode = path.pop()
      pnode.size -= 1
      pnode.valsize -= lmax_val if fdi & 1 else 1
      fdi >>= 1

    return True

  def discard(self, key, val=1) -> bool:
    path = []
    node = self.node
    while node is not None:
      path.append(node)
      if key == node.key:
        break
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    else:
      return False
    if val > node.val:
      val = node.val - 1
      node.val -= val
      for p in path:
        p.valsize -= val
    if node.val == 1:
      self._discard(key)
    else:
      node.val -= val
      for p in path:
        p.valsize -= val
    return True

  def discard_all(self, key) -> None:
    self.discard(key, self.count(key))
    return

  def add(self, key, val=1) -> None:
    if self.node is None:
      self.node = Node(key, val)
      return
    pnode = self.node
    di = 0
    path = []
    while pnode is not None:
      if key == pnode.key:
        pnode.val += val
        pnode.valsize += val
        for p in path:
          p.valsize += val
        return
      elif key < pnode.key:
        path.append(pnode)
        di <<= 1
        di |= 1
        pnode = pnode.left
      else:
        path.append(pnode)
        di <<= 1
        pnode = pnode.right
    if di & 1:
      path[-1].left = Node(key, val)
    else:
      path[-1].right = Node(key, val)
    new_node = None
    while path:
      pnode = path.pop()
      pnode.size += 1
      pnode.valsize += val
      pnode.balance += 1 if di & 1 else -1
      di >>= 1
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance < 0 else self._rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance> 0 else self._rotate_R(pnode)
        break
    if new_node is not None:
      if path:
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
      else:
        self.node = new_node
    for p in path:
      p.size += 1
      p.valsize += val
    return

  def count(self, key) -> int:
    node = self.node
    while node is not None:
      if node.key == key:
        return node.val
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return 0

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
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
        res = key
        break
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

  def pop(self, k: int=-1) -> T:
    x = self._kth_elm(k)[0]
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

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.to_l_items())) + '}')

  def get_elm(self, k: int) -> T:
    return self._kth_elm_tree(k)[0]

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

  def __getitem__(self, k):
    return self._kth_elm(k)[0]

  def __contains__(self, key):
    node = self.node
    while node:
      if node.key == key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self._kth_elm(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self._kth_elm(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return True if self.node is not None else False

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'AVLTreeMultiSet ' + str(self)

