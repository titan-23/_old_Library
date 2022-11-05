class Node:

  def __init__(self, key):
    self.key = key
    self.size = 1
    self.left = None
    self.right = None

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size}\n'
    return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeSet:

  def __init__(self, a=[]) -> None:
    if a:
      aa = sorted(a)
      a = [aa[0]]
      for i in range(1, len(aa)):
        if aa[i] != a[-1]:
          a.append(aa[i])
    self.node = self.__build(a)
 
  def __build(self, a: list) -> None:
    def sort(l, r):
      if l >= r:
        return None, 0
      mid = (l + r) >> 1
      root = Node(a[mid])
      root.left, sl = sort(l, mid)
      root.right, sr = sort(mid+1, r)
      root.size = sl+sr+1
      return root, sl+sr+1
    return sort(0, len(a))[0]

  def __update(self, node):
    if node is None: return
    node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)

  def __splay(self, node, path, di):
    while len(path) > 1:
      node = path.pop()
      pnode = path.pop()
      ndi = di & 1
      pdi = di >> 1 & 1
      di >>= 2

      if ndi == pdi:
        if ndi == 1:
          pnode.left = node.right
          node.right = pnode
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          self.__update(tmp.right.right)
          self.__update(tmp.right)
          self.__update(tmp)
        else:
          pnode.right = node.left
          node.left = pnode
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          self.__update(tmp.left.left)
          self.__update(tmp.left)
          self.__update(tmp)
      else:
        if ndi == 1:
          tmp = node.left
          pnode.right = tmp.left
          tmp.left = pnode
          node.left = tmp.right
          tmp.right = node
          self.__update(tmp.left)
          self.__update(tmp.right)
          self.__update(tmp)
        else:
          tmp = node.right
          pnode.left = tmp.right
          tmp.right = pnode
          node.right = tmp.left
          tmp.left = node
          self.__update(tmp.left)
          self.__update(tmp.right)
          self.__update(tmp)
      if not path:
        return tmp
      if di & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp

    if not path:
      return node
    gnode = path.pop()
    if di & 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
      self.__update(node.right)
      self.__update(node)
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self.__update(node.left)
      self.__update(node)
    return node

  def __search_splay(self, key):
    node = self.node
    if node is None:
      return
    path = []
    di = 0
    while node is not None:
      if node.key == key:
        self.node = self.__splay(node, path, di)
        return
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        node = node.left
      else:
        di = di << 1
        path.append(node)
        node = node.right
    node = path.pop()
    di >>= 1
    if not path:
      self.node = node
      return
    self.node = self.__splay(self.node, path, di)
    return

  def add(self, key):
    if self.node is None:
      self.node = Node(key)
      return True
    self.__search_splay(key)
    if self.node.key == key:
      return False
    node = Node(key)
    if key < self.node.key:
      node.right = self.node
      node.left = self.node.left
      self.node.left = None
      self.__update(node.right)
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
      self.__update(node.left)
    self.node = node
    self.__update(self.node)
    return True

  def __search_min_splay(self, node):
    path = []
    root = node
    while node is not None:
      path.append(node)
      node = node.left
    if not path:
      return root
    if len(path) == 1:
      return root
    node = path.pop()
    if not path:
      return node
    return self.__splay(root, path, (1<<len(path))-1)

  def discard(self, key):
    if self.node is None:
      return False
    self.__search_splay(key)
    if self.node.key != key:
      return False
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self.__search_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
      self.__update(self.node.left)
    self.__update(self.node)
    return True

  def __contains__(self, key):
    self.__search_splay(key)
    return self.node is not None and self.node.key == key

  def __kth_elm(self, k):
    if k < 0:
      k += self.__len__()
    now = 0
    node = self.node
    path = []
    di = 0
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t == k:
        self.node = self.__splay(self.node, path, di)
        return self.node.key
      elif t < k:
        di = di << 1
        path.append(node)
        now = t + 1
        node = node.right
      else:
        di = di << 1 | 1
        path.append(node)
        node = node.left
    raise IndexError(f'k={k}, len={self.__len__()}')

  def __getitem__(self, indx):
    return self.__kth_elm(indx)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    path = []
    res = None
    di = 0
    node = self.node
    if node is None:
      return None
    while node is not None:
      if node.key == key:
        self.node = self.__splay(self.node, path, di)
        return key
      elif key < node.key:
        di = di << 1 | 1
        path.append(node)
        node = node.left
      else:
        di = di << 1
        path.append(node)
        res = node.key
        node = node.right
    node = path.pop()
    di >>= 1
    if not path:
      self.node = node
    else:
      self.node = self.__splay(self.node, path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    path = []
    res = None
    di = 0
    node = self.node
    if node is None:
      return None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        di = di << 1 | 1
        path.append(node)
        node = node.left
      else:
        di = di << 1
        path.append(node)
        res = node.key
        node = node.right
    node = path.pop()
    di >>= 1
    if not path:
      self.node = node
    else:
      self.node = self.__splay(self.node, path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    path = []
    res = None
    di = 0
    node = self.node
    if node is None:
      return None
    while node is not None:
      if node.key == key:
        self.node = self.__splay(self.node, path, di)
        return key
      elif key < node.key:
        di = di << 1 | 1
        path.append(node)
        res = node.key
        node = node.left
      else:
        di = di << 1
        path.append(node)
        node = node.right
    node = path.pop()
    di >>= 1
    if not path:
      self.node = node
    else:
      self.node = self.__splay(self.node, path, di)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    path = []
    res = None
    di = 0
    node = self.node
    if node is None:
      return None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        di = di << 1 | 1
        path.append(node)
        res = node.key
        node = node.left
      else:
        di = di << 1
        path.append(node)
        node = node.right
    node = path.pop()
    di >>= 1
    if not path:
      self.node = node
    else:
      self.node = self.__splay(self.node, path, di)
    return res

  def __str__(self):
    return '{' + ', '.join(map(str, [self.__getitem__(i) for i in range(self.__len__())])) + '}'


