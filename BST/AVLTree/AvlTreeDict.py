# https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AvlTreeDict.py


from typing import Callable, Generic, Iterable, Tuple, TypeVar, Union, List, Any
T = TypeVar("T")


class Node:

  def __init__(self, key, val: Any):
    self.key = key
    self.val = val
    self.size = 1
    self.left = None
    self.right = None
    self.balance = 0

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val, self.size}\n'
    return f'key:{self.key, self.val, self.size},\n left:{self.left},\n right:{self.right}\n'


class AVLTreeDict(Generic[T]):

  def __init__(self, a: Iterable[T]=[], c: bool=False, default: Callable[[], T]=None) -> None:
    self._default = default
    self.node = None
    if c:
      self._default = int
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    for a_ in sorted(a):
      self.__setitem__(a_, self.__getitem__(a_)+1)

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    node.size -= 1 if u.left is None else u.left.size + 1
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
    node.size -= 1 if u.right is None else u.right.size + 1
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
    if E.right is None:
      node.size -= B.size
      B.size -= 1
    else:
      node.size -= B.size - E.right.size
      B.size -= E.right.size + 1
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
    if D.left is None:
      node.size -= C.size
      C.size -= 1
    else:
      node.size -= C.size - D.left.size
      C.size -= D.left.size + 1
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def _kth_elm(self, k: int) -> Node:
    if k < 0:
      k += self.__len__()
    assert 0 <= k < self.__len__()
    node = self.node
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def items(self):
    for i in range(self.__len__()):
      yield self._kth_elm(i)

  def keys(self):
    for i in range(self.__len__()):
      yield self._kth_elm(i)[0]

  def values(self):
    for i in range(self.__len__()):
      yield self._kth_elm(i)[1]

  def _search_node(self, key: T) -> Union[Node, None]:
    node = self.node
    while node is not None:
      if key == node.key:
        return node
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return None

  def _discard(self, key: T) -> bool:
    di = 0
    path = []
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
    else:
      return False
    if node.left is not None and node.right is not None:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = node.left
      while lmax.right is not None:
        path.append(lmax)
        di <<= 1
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      pnode = path[-1]
      if di & 1:
        pnode.left = cnode
      else:
        pnode.right = cnode
    else:
      self.node = cnode
      return True
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1 if di & 1 else -1
      di >>= 1
      pnode.size -= 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return True
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
        if new_node.balance != 0:
          break
    for p in path:
      p.size -= 1
    return True

  def __setitem__(self, key: T, val: Any):
    if self.node is None:
      self.node = Node(key, val)
      return True
    pnode = self.node
    path = []
    di = 0
    while pnode is not None:
      if key == pnode.key:
        pnode.val = val
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
      pnode.balance += 1 if di & 1 else -1
      di >>= 1
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
        break
    if new_node is not None:
      if path:
        gnode = path.pop()
        gnode.size += 1
        if di & 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
      else:
        self.node = new_node
    for p in path:
      p.size += 1
    return True

  def __delitem__(self, key: T):
    if self._discard(key):
      return
    raise KeyError(key)

  def __getitem__(self, key: T):
    node = self._search_node(key)
    return self.__missing__() if node is None else node.val

  def __contains__(self, key: T):
    return self._search_node(key) is not None

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self._kth_elm(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __repr__(self):
    return 'AVLTreeDict ' + str(self)

  def __missing__(self):
    return self._default()

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self._kth_elm(self.__iter)[0]
    self.__iter += 1
    return res

