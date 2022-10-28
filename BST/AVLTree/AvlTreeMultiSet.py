class Node:
  # __slots__ = ('key', 'val', 'size', 'valsize', 'left', 'right', 'balance')
  
  def __init__(self, key, val: int):
    self.key = key
    self.val = val
    self.valsize = val
    self.size = 1
    self.left = None
    self.right = None
    self.balance = 0


class AVLTreeMultiSet:

  # __slots__ = ('node', '__iter')

  # __LEFT, __RIGHT = 1, -1

  def __init__(self, V=[]):
    self.node = None
    self.__build(V)

  def __build(self, V):
    for v in sorted(V):
      self.add(v)

  def __rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    u.valsize = node.valsize
    node.size -= 1 if u.left is None else u.left.size + 1
    node.valsize -= u.val if u.left is None else u.left.valsize + u.val
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
    u.valsize = node.valsize
    node.size -= 1 if u.right is None else u.right.size + 1
    node.valsize -= u.val if u.right is None else u.right.valsize + u.val
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
    E = node.left.right
    F1 = E.left
    F2 = E.right
    E.left = node.left
    E.left.right = F1
    E.right = node
    E.right.left = F2

    E.left.size = 1 + (0 if E.left.right is None else E.left.right.size) + (0 if E.left.left is None else E.left.left.size)
    E.right.size = 1 + (0 if E.right.right is None else E.right.right.size) + (0 if E.right.left is None else E.right.left.size)
    E.size = 1 + E.left.size + E.right.size

    E.left.valsize = E.left.val + (0 if E.left.right is None else E.left.right.valsize) + (0 if E.left.left is None else E.left.left.valsize)
    E.right.valsize = E.right.val + (0 if E.right.right is None else E.right.right.valsize) + (0 if E.right.left is None else E.right.left.valsize)
    E.valsize = E.left.valsize + E.right.valsize + E.val

    self.__update_balance(E)
    return E

  def __rotate_RL(self, node: Node) -> Node:
    D = node.right.left
    F1 = D.left
    F2 = D.right
    D.right = node.right
    D.right.left = F2
    D.left = node
    D.left.right = F1

    D.left.size = 1 + (0 if D.left.left is None else D.left.left.size) + (0 if D.left.right is None else D.left.right.size)
    D.right.size = 1 + (0 if D.right.left is None else D.right.left.size) + (0 if D.right.right is None else D.right.right.size)
    D.size = 1 + D.right.size + D.left.size

    D.left.valsize = D.left.val + (0 if D.left.left is None else D.left.left.valsize) + (0 if D.left.right is None else D.left.right.valsize)
    D.right.valsize = D.right.val + (0 if D.right.left is None else D.right.left.valsize) + (0 if D.right.right is None else D.right.right.valsize)
    D.valsize = D.right.valsize + D.left.valsize + D.val
    
    self.__update_balance(D)
    return D

  def __discard(self, key) -> bool:
    '''Discard node of key from self. / O(logN)'''
    path = []
    node = self.node
    while node is not None:
      if key < node.key:
        path.append((node, 1, 0))
        node = node.left
      elif key > node.key:
        path.append((node, -1, 0))
        node = node.right
      else:
        break

    if node.left is not None and node.right is not None:
      path.append((node, 1, 0))
      lmax = node.left
      while lmax.right is not None:
        path.append((lmax, -1, 1))
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax

    cnode = node.right if node.left is None else node.left
    if path:
      pnode, di, _ = path[-1]
      if di == 1:
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
      pnode.valsize -= lmax_val if flag else 1

      if pnode.balance == 2:
        new_node = self.__rotate_LR(pnode) if pnode.left.balance < 0 else self.__rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self.__rotate_RL(pnode) if pnode.right.balance> 0 else self.__rotate_R(pnode)
      elif pnode.balance != 0:
        break

      if new_node is not None:
        if not path:
          self.node = new_node
          return    
        gnode, gdir, _ = path[-1]
        if gdir == 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
        if new_node.balance != 0:
          break

    while path:
      pnode, _, flag = path.pop()
      pnode.size -= 1
      pnode.valsize -= lmax_val if flag else 1

    return True

  def discard(self, key, cnt=1) -> bool:
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
    if cnt > node.val:
      cnt = node.val - 1
      node.val -= cnt
      while path:
        path.pop().valsize -= cnt
    if node.val == 1:
      self.__discard(key)
    else:
      node.val -= cnt
      while path:
        path.pop().valsize -= cnt
    return True

  def discard_all(self, key) -> None:
    self.discard(key, self.count(key))
    return

  def __getval(self, key):
    node = self.node
    while node:
      if node.key == key:
        return node.val
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    raise KeyError

  def add(self, key, cnt=1) -> None:
    '''add key cnt times. / O(logN)'''
    if self.node is None:
      self.node = Node(key, cnt)
      return

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
        pnode.val += cnt
        pnode.valsize += cnt
        while path:
          path.pop()[0].valsize += cnt
        return

    pnode, di = path[-1]
    if di == 1:
      pnode.left = Node(key, cnt)
    else:
      pnode.right = Node(key, cnt)
    
    new_node = None
    while path:
      pnode, di = path.pop()
      pnode.size += 1
      pnode.valsize += cnt
      pnode.balance += di
      if pnode.balance == 0:
        break

      if pnode.balance == 2:
        new_node = self.__rotate_LR(pnode) if pnode.left.balance < 0 else self.__rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self.__rotate_RL(pnode) if pnode.right.balance> 0 else self.__rotate_R(pnode)
        break
      # if pnode.balance == 2:  # pnodeの左部分木が茂りすぎ
      #   if pnode.left.balance < 0:
      #     # LR2重回転: nodeの右側が茂っている場合
      #     new_node = self.__rotate_LR(pnode)
      #   else:
      #     # LL1重回転: nodeの左側が茂っている場合
      #     new_node = self.__rotate_L(pnode)
      #   break
      # elif pnode.balance == -2:   # pnodeの右部分木が茂りすぎ
      #   if pnode.right.balance > 0:
      #     # RL2重回転: nodeの左側が茂っている場合
      #     new_node = self.__rotate_RL(pnode)
      #   else:
      #     # RR1重回転: nodeの右側が茂っている場合
      #     new_node = self.__rotate_R(pnode)
      #   break
      # else: 最初にpnode.balanceを更新したので、何もせずcontinueしてOK

    if new_node is not None:
      if path:
        gnode, gdi = path[-1]
        if gdi == 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
      else:
        self.node = new_node

    while path:
      pnode, _ = path.pop()
      pnode.size += 1
      pnode.valsize += cnt
    return

  '''Count the numer of key. / O(logN)'''
  def count(self, key) -> int:
    return self.__getval(key)

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    res, node = None, self.node
    while node is not None:
      if key < node.key:
        node = node.left
      elif key > node.key:
        res, node = node.key, node.right
      else:
        return key
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    res, node = None, self.node
    while node is not None:
      if key < node.key:
        node = node.left
      elif key > node.key:
        res, node = node.key, node.right
      else:
        break
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    res, node = None, self.node
    while node is not None:
      if key < node.key:
        res, node = node.key, node.left
      elif key > node.key:
        node = node.right
      else:
        return key
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    res, node = None, self.node
    while node is not None:
      if key < node.key:
        res, node = node.key, node.left
      elif key > node.key:
        node = node.right
      else:
        break
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        indx += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
      else:
        indx += 0 if node.left is None else node.left.valsize
        break
    return indx

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        indx += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
      else:
        indx += node.val if node.left is None else node.left.valsize + node.val
        break
    return indx

  def pop(self, p=-1):
    '''Return and Remove max element or a[p]. / O(logN)'''
    if p < 0:
      p += self.__len__()
    assert 0 <= p < self.__len__()
    x = self.__getitem__(p)
    self.discard(x)
    return x

  def popleft(self):
    '''Return and Remove min element. / O(logN)'''
    return self.pop(0)

  def items(self):
    for i in range(self.__len_tree()):
      yield self.__kth_elm_tree(i)

  def keys(self):
    for i in range(self.__len_tree()):
      yield self.__kth_elm_tree(i)[0]

  def values(self):
    for i in range(self.__len_tree()):
      yield self.__kth_elm_tree(i)[1]

  def __getitem__(self, k):
    return self.__kth_elm_set(k)[0]

  def __kth_elm_set(self, k) -> tuple:
    if k < 0:
      k += self.__len__()
    now = 0
    node = self.node
    while node is not None:
      s = now + node.left.valsize if node.left is not None else now
      t = s + node.val
      if s <= k < t:
        return node.key, node.val
      elif t <= k:
        now = t
        node = node.right
      else:
        node = node.left
    raise IndexError

  def __kth_elm_tree(self, k) -> tuple:
    if k < 0:
      k += self.__len_tree()
    now = 0
    node = self.node
    while node is not None:
      t = now + node.left.size if node.left is not None else now
      if t == k:
        return node.key, node.val
      elif t < k:
        now = t + 1
        node = node.right
      else:
        node = node.left
    raise IndexError

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
    res = self.__kth_elm_set(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__kth_elm_set(-i-1)

  def __len_tree(self):
    return 0 if self.node is None else self.node.size

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return True if self.node is not None else False

  def __str__(self):
    return '{' + ', '.join(map(lambda x: ', '.join([str(x[0])]*x[1]), self.items())) + '}'

  def show(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __str__(self):
    return '{' + ', '.join(map(lambda x: ', '.join([str(x[0])]*x[1]), self.items())) + '}'

  def len_elm(self):
    return self.__len_tree()


