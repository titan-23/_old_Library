from typing import Generic, Iterable, Tuple, TypeVar, Union, List
T = TypeVar("T")


class Node:

  def __init__(self, key, val: int):
    self.key = key
    self.val = val
    self.left = None
    self.right = None
    self.balance = 0

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val}\n'
    return f'key:{self.key, self.val},\n left:{self.left},\n right:{self.right}\n'


class AVLTreeMultiSet2(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:  
    self.node = None
    self._len = 0
    self._len_elm = 0
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
        node.balance = hl
        h = hl
      if mid+1 != r:
        right, hr = sort(mid+1, r)
        node.right = right
        node.balance -= hr
        if hr > h:
          h = hr
      return node, h+1
    a = sorted(a)
    self._len = len(a)
    a = self._rle(a)
    self._len_elm = len(a)
    self.node = sort(0, len(a))[0]

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
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
    B.right = E.left
    E.left = B
    node.left = E.right
    E.right = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: Node) -> Node:
    C = node.right
    D = C.left
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def _discard(self, key: T) -> bool:
    path = []
    di = 0
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
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di & 1 == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
      return True
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1 if di & 1 == 1 else -1
      di >>= 1
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
    return True

  def remove(self, key: T, val: int=1) -> None:
    if not self.discard(key, val):
      raise KeyError(key)

  def discard(self, key: T, val: int=1) -> bool:
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
    self._len -= val if val < node.val else node.val
    if val > node.val:
      val = node.val - 1
      node.val -= val
    if node.val == 1:
      self._len_elm -= 1
      self._discard(key)
    else:
      node.val -= val
    return True

  def discard_all(self, key: T) -> None:
    self.discard(key, self.count(key))

  def add(self, key: T, val: int=1) -> None:
    self._len += val
    if self.node is None:
      self._len_elm += 1
      self.node = Node(key, val)
      return
    pnode = self.node
    di = 0
    path = []
    while pnode is not None:
      if key == pnode.key:
        pnode.val += val
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
    self._len_elm += 1
    if di & 1 == 1:
      path[-1].left = Node(key, val)
    else:
      path[-1].right = Node(key, val)
    new_node = None
    for _ in range(len(path)):
      pnode = path.pop()
      pnode.balance += 1 if di & 1 == 1 else -1
      di >>= 1
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance < 0 else self._rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance > 0 else self._rotate_R(pnode)
        break
    if new_node is not None:
      if path:
        if di & 1 == 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
      else:
        self.node = new_node
    return

  def count(self, key: T) -> int:
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
      if key <= node.key:
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
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def pop(self) -> T:
    self._len -= 1
    path = []
    node = self.node
    while node.right is not None:
      path.append(node)
      node = node.right
    res = node.key
    if node.val > 1:
      node.val -= 1
      return res
    self._len_elm -= 1
    cnode = node.right if node.left is None else node.left
    if path:
      path[-1].right = cnode
    else:
      self.node = cnode
      return res
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance += 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return res
        path[-1].right = new_node
        if new_node.balance != 0:
          break
    return res

  def popleft(self) -> T:
    self._len -= 1
    path = []
    node = self.node
    while node.left is not None:
      path.append(node)
      node = node.left
    res = node.key
    if node.val > 1:
      node.val -= 1
      return res
    self._len_elm -= 1
    cnode = node.right if node.left is None else node.left
    if path:
      path[-1].left = cnode
    else:
      self.node = cnode
      return res
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1
      if pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return res
        path[-1].left = new_node
        if new_node.balance != 0:
          break
    return res

  def get_min(self) -> T:
    node = self.node
    while node.left is not None:
      node = node.left
    return node.key

  def get_max(self) -> T:
    node = self.node
    while node.right is not None:
      node = node.right
    return node.key

  def len_elm(self) -> int:
    return self._len_elm

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.to_l_items())) + '}')

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
    while node:
      if node.key == key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __getitem__(self, k):  # 先頭と末尾しか対応していない
    if k == -1 or k == self._len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __len__(self):
    return self._len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'AVLTreeMultiSet2' + str(self)


