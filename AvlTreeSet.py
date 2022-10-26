class Node:
  # __slots__ = ('key', 'size', 'left', 'right', 'balance')
  
  def __init__(self, key):
    self.key = key
    self.size = 1
    self.left = None
    self.right = None
    self.balance = 0

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size}\n'
    return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'


class AVLTreeSet:

  # __slots__ = ('node', '__iter')

  '''Make a new AVLTree.'''
  def __init__(self, a=[]) -> None:  
    # V: Iterable
    a = sorted(a)
    self.node = None
    self.__len = 0
    if a:
      aa = [a[0]]
      for i in range(1, len(a)):
        if a[i] != aa[-1]:
          aa.append(a[i])
      self.__len = len(aa)
      self.__build(aa)

  def __build(self, a) -> None:
    def sort(l, r):
      if l >= r:
        return None, 0
      mid = (l + r) // 2
      root = Node(a[mid])
      root.left, hl = sort(l, mid)
      root.right, hr = sort(mid+1, r)
      root.balance = hl - hr
      if root.left is not None:
        root.size += root.left.size
      if root.right is not None:
        root.size += root.right.size
      return root, max(hl, hr)+1
    self.node = sort(0, len(a))[0]

  def __rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    node.size -= 1 if u.left is None else u.left.size + 1
    node.left = u.right
    u.right = node
    if u.balance == 1:
      u.balance, node.balance = 0, 0
    else:
      u.balance, node.balance = -1, 1
    return u

  def __rotate_R(self, node: Node) -> Node:
    u = node.right
    u.size = node.size
    node.size -= 1 if u.right is None else u.right.size + 1
    node.right = u.left
    u.left = node
    if u.balance == -1:
      u.balance, node.balance = 0, 0
    else:
      u.balance, node.balance = 1, -1
    return u

  def __update_balance(self, node: Node) -> None:
    # nodeはnew_node
    if node.balance == 1:
      node.right.balance, node.left.balance = -1, 0
    elif node.balance == -1:
      node.right.balance, node.left.balance = 0, 1
    else:
      node.right.balance, node.left.balance = 0, 0
    node.balance = 0

  def __rotate_LR(self, node: Node) -> Node:
    #      A           E
    #     / \         / \
    #    B   C  ->   B   A
    #   /\          /\   /\
    #  D  E        D  F1F2 C
    #    /\
    #   F1 F2
    # # node: A
    B = node.left
    E = B.right
    E.size = node.size
    ers = 0 if E.right is None else E.right.size
    node.size -= B.size - ers
    B.size -= ers + 1
    B.right = E.left
    E.left = B
    node.left = E.right
    E.right = node
    self.__update_balance(E)
    return E

  def __rotate_RL(self, node: Node) -> Node:
    C = node.right
    D = C.left
    D.size = node.size
    dls = 0 if D.left is None else D.left.size
    node.size -= C.size - dls
    C.size -= dls + 1
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self.__update_balance(D)
    return D

  '''add a key. / O(logN)'''
  def add(self, key) -> bool:
    if self.node is None:
      self.node = Node(key)
      return True

    pnode = self.node
    path = []
    while pnode is not None:
      if key < pnode.key:
        path.append((pnode, 1))
        pnode = pnode.left
      elif key > pnode.key:
        path.append((pnode, -1))
        pnode = pnode.right
      else:
        return False

    pnode, di = path[-1]
    if di == 1:
      pnode.left = Node(key)
    else:
      pnode.right = Node(key)
    
    while path:
      new_node = None
      pnode, di = path.pop()
      pnode.size += 1
      pnode.balance += di
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self.__rotate_LR(pnode) if pnode.left.balance == -1 else self.__rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self.__rotate_RL(pnode) if pnode.right.balance == 1 else self.__rotate_R(pnode)
        break

    if new_node is not None:
      if path:
        gnode, gdi = path.pop()
        gnode.size += 1
        if gdi == 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
      else:
        self.node = new_node
        return

    while path:
      path.pop()[0].size += 1
    
    return True

  '''Remove key. / O(logN)'''
  def remove(self, key) -> bool:
    if self.discard(key):
      return True
    raise KeyError(f'{key} is not exist.')

  '''Discard key. / O(logN)'''
  def discard(self, key) -> bool:
    path = []
    node = self.node
    while node is not None:
      if key < node.key:
        path.append((node, 1))
        node = node.left
      elif key > node.key:
        path.append((node, -1))
        node = node.right
      else:
        break
    else:
      return False

    if node.left is not None and node.right is not None:
      path.append((node, 1))
      lmax = node.left
      while lmax.right is not None:
        path.append((lmax, -1))
        lmax = lmax.right
      node.key = lmax.key
      node = lmax

    cnode = node.right if node.left is None else node.left
    if path:
      pnode, di = path[-1]
      if di == 1:
        pnode.left = cnode
      else:
        pnode.right = cnode
    else:
      self.node = cnode
      return True

    while path:
      new_node = None
      pnode, di = path.pop()
      pnode.balance -= di
      pnode.size -= 1

      if pnode.balance == 2:
        new_node = self.__rotate_LR(pnode) if pnode.left.balance == -1 else self.__rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self.__rotate_RL(pnode) if pnode.right.balance == 1 else self.__rotate_R(pnode)
      elif pnode.balance != 0:
        break

      if new_node is not None:
        if not path:
          self.node = new_node
          return    
        gnode, gdir = path[-1]
        if gdir == 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
        if new_node.balance != 0:
          break

    while path:
      path.pop()[0].size -= 1

    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        node = node.left
      elif key > node.key:
        res = node.key
        node = node.right
      else:
        res = key
        break
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        node = node.left
      elif key > node.key:
        res = node.key
        node = node.right
      else:
        break
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      elif key > node.key:
        node = node.right
      else:
        res = key
        break
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      elif key > node.key:
        node = node.right
      else:
        break
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key) -> int:
    indx = 0
    node = self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        indx += 1 if node.left is None else node.left.size + 1
        node = node.right
      else:
        indx += 0 if node.left is None else node.left.size
        break
    return indx

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    indx = 0
    node = self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        indx += 1 if node.left is None else node.left.size + 1
        node = node.right
      else:
        indx += 1 if node.left is None else node.left.size + 1
        break
    return indx

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p=-1):
    if p < 0:
      p += self.__len__()
    x = self.__kth_elm(p)
    self.discard(x)
    return x

  '''Return and Remove min element. / O(logN)'''
  def popleft(self):
    return self.pop(0)

  def __kth_elm(self, k):
    if k < 0:
      k += self.__len__()
    now = 0
    node = self.node
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t < k:
        now = t + 1
        node = node.right
      elif t > k:
        node = node.left
      else:
        return node.key
    raise IndexError(f'k={k}, len={self.__len__()}')

  def __contains__(self, x):
    node = self.node
    while node:
      if x < node.key:
        node = node.left
      elif x > node.key:
        node = node.right
      else:
        return True
    return False

  def __getitem__(self, x):
    return self.__kth_elm(x)

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

  def __bool__(self):
    return self.node is not None

  def __repr__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

