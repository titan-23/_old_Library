class Node:
  __slots__ = ('key', 'val', 'size', 'left', 'right', 'balance')

  def __init__(self, key, val):
    self.key = key
    self.val = val
    self.size = 1
    self.left = None
    self.right = None
    self.balance = 0


class AVLTreeDict:
  
  __slots__ = ('node', '__iter', '__default')

  __LEFT, __RIGHT = 1, -1

  def __init__(self, V=[], c=False, default=None) -> None:
    self.__default = default
    self.node = None
    if c:
      self.__default = int
      self.__build(V)

  def __build(self, V) -> None:
    for v in sorted(V):
      self.__setitem__(v, self.__getitem__(v)+1)

  def __rotate_L(self, node: Node) -> Node:
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

  def __rotate_R(self, node: Node) -> Node:
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

  def __update_balance(self, node: Node) -> None:
    # nodeはnew_node
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

  def __kth_elm(self, k: int) -> tuple:
    if k < 0:
      k += self.__len__()
    now = 0
    node = self.node
    while node is not None:
      t =  now if node.left is None else now + node.left.size
      if t < k:
        now = t + 1
        node = node.right
      elif t > k:
        node = node.left
      else:
        return node.key, node.val
    raise IndexError(f'k={k}, len={self.__len__()}')

  def items(self) -> tuple:
    indx = 0
    while indx < self.__len__():
      yield self.__kth_elm(indx)
      indx += 1

  def keys(self):
    indx = 0
    while indx < self.__len__():
      yield self.__kth_elm(indx)[0]
      indx += 1

  def values(self):
    indx = 0
    while indx < self.__len__():
      yield self.__kth_elm(indx)[1]
      indx += 1

  def __search_node(self, key) -> Node:
    node = self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        node = node.right
      else:
        break
    return node

  def __discard(self, key) -> bool:
    '''Discard a key. / O(logN)'''
    path = []
    node = self.node
    while node is not None:
      if key < node.key:
        path.append((node, self.__LEFT, 0))
        node = node.left
      elif key > node.key:
        path.append((node, self.__RIGHT, 0))
        node = node.right
      else:
        break
    else:
      return False

    if node.left is not None and node.right is not None:
      path.append((node, self.__LEFT, 0))
      lmax = node.left
      while lmax.right is not None:
        path.append((lmax, self.__RIGHT, 1))
        lmax = lmax.right
      node.key = lmax.key
      node.val = lmax.val
      lmax_val = lmax.val
      node = lmax

    cnode = node.right if node.left is None else node.left
    if path:
      pnode, di, _ = path[-1]
      if di == self.__LEFT:
        pnode.left = cnode
      else:
        pnode.right = cnode
    else:
      self.node = cnode
      return True

    while path:
      new_node = None
      pnode, di, flag = path.pop()
      pnode.balance -= di
      pnode.size -= 1

      if pnode.balance > 1:
        if pnode.left.balance < 0:
          new_node = self.__rotate_LR(pnode)
        else:
          new_node = self.__rotate_L(pnode)
      elif pnode.balance < -1:
        if pnode.right.balance > 0:
          new_node = self.__rotate_RL(pnode)
        else:
          new_node = self.__rotate_R(pnode)
      elif pnode.balance != 0:
        break

      if new_node is not None:
        if not path:
          self.node = new_node
          return    
        gnode, gdir, _ = path[-1]
        if gdir == self.__LEFT:
          gnode.left = new_node
        else:
          gnode.right = new_node
        if new_node.balance != 0:
          break

    while path:
      path.pop()[0].size -= 1

    return True

  def __setitem__(self, key, val):
    '''add a key. / O(logN)'''
    if self.node is None:
      self.node = Node(key, val)
      return True

    pnode = self.node
    path = []
    while pnode is not None:
      if key < pnode.key:
        path.append((pnode, self.__LEFT))
        pnode = pnode.left
      elif key > pnode.key:
        path.append((pnode, self.__RIGHT))
        pnode = pnode.right
      else:
        pnode.val = val
        return

    pnode, di = path[-1]
    if di == self.__LEFT:
      pnode.left = Node(key, val)
    else:
      pnode.right = Node(key, val)
    
    while path:
      new_node = None
      pnode, di = path.pop()
      pnode.size += 1
      pnode.balance += di
      if pnode.balance == 0:
        break

      if pnode.balance > 1:  # pnodeの左部分木が茂りすぎ
        if pnode.left.balance < 0:
          # LR2重回転: nodeの右側が茂っている場合
          new_node = self.__rotate_LR(pnode)
        else:
          # LL1重回転: nodeの左側が茂っている場合
          new_node = self.__rotate_L(pnode)
        break
      elif pnode.balance < -1:   # pnodeの右部分木が茂りすぎ
        if pnode.right.balance > 0:
          # RL2重回転: nodeの左側が茂っている場合
          new_node = self.__rotate_RL(pnode)
        else:
          # RR1重回転: nodeの右側が茂っている場合
          new_node = self.__rotate_R(pnode)
        break
      # else: 最初にpnode.balanceを更新したので、何もせずcontinueしてOK

    if new_node is not None:
      if path:
        gnode, gdi = path.pop()
        gnode.size += 1
        if gdi == self.__LEFT:
          gnode.left = new_node
        else:
          gnode.right = new_node
      else:
        self.node = new_node
        return

    while path:
      path.pop()[0].size += 1

    return

  def __delitem__(self, key):
    '''Remove a key. / O(logN)'''
    if self.__discard(key):
      return
    raise KeyError(key)

  def __getitem__(self, key):
    node = self.__search_node(key)
    return self.__missing__() if node is None else node.val

  def __contains__(self, key):
    return self.__search_node(key) is not None

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__kth_elm(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __repr__(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __str__(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __missing__(self):
    return self.__default()

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__kth_elm(self.__iter)[0]
    self.__iter += 1
    return res


