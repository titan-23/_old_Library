class Node:

  def __init__(self, key):
    self.key = key
    self.size = 1
    self.left = None
    self.right = None
    self.data = key

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.data, self.size}\n'
    return f'key:{self.key, self.data, self.size},\n left:{self.left},\n right:{self.right}\n'


class SplayTree:

  def __init__(self, _a=[], node=None, op=lambda x,y: min(x, y)) -> None:
    self.node = node
    self.op = op
    if _a:
      self.node = self._build(list(_a))
 
  def _build(self, a: list) -> None:
    def sort(l, r):
      if l >= r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left, node.right = sort(l, mid), sort(mid+1, r)
      self._update(node)
      return node
    return sort(0, len(a))

  def _update(self, node) -> None:
    if node is None: return
    node.size, node.data = 1, node.key
    if node.left is not None:
      node.size += node.left.size
      node.data = self.op(node.left.data, node.data)
    if node.right is not None:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)

  def _splay(self, node, path, di) -> Node:
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
        else:
          pnode.right = node.left
          node.left = pnode
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
      else:
        if ndi == 1:
          tmp = node.left
          pnode.right = tmp.left
          tmp.left = pnode
          node.left = tmp.right
          tmp.right = node
        else:
          tmp = node.right
          pnode.left = tmp.right
          tmp.right = pnode
          node.right = tmp.left
          tmp.left = node
      self._update(pnode)
      self._update(node)
      self._update(tmp)
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
      self._update(node.right)
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self._update(node.left)
    self._update(node)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    now, di = 0, 0
    node, path = self.node, []
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t == k:
        self.node = self._splay(self.node, path, di)
        return
      elif t < k:
        path.append(node)
        di, node = di<<1, node.right
        now = t + 1
      else:
        path.append(node)
        di, node = di<<1|1, node.left
    raise IndexError(f'k={k}, len={self.__len__()}')

  def _get_min_splay(self, node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(node, path, (1<<len(path))-1)

  def _get_max_splay(self, node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(node, path, 0)

  def merge(self, other) -> None:
    self.node = self._get_max_splay(self.node)
    if self.node:
      self.node.right = other._get_min_splay(other.node)
    else:
      self.node = other._get_min_splay(other.node)
    self._update(self.node)

  def split(self, indx, inc=False) -> tuple:
    if indx >= self.__len__():
      return self, SplayTree(node=None)
    self._set_kth_elm_splay(indx)
    if inc:
      right = SplayTree(node=self.node.right, op=self.op)
      self.node.right = None
      left = self
      self._update(left.node)
    else:
      left = SplayTree(node=self.node.left, op=self.op)
      self.node.left = None
      right = self
      self._update(right.node)
    return left, right

  def prod(self, l: int, r: int):
    left, right = self.split(r-1, inc=True)
    lleft, lright = left.split(l)
    res = lright.node.data
    lleft.merge(lright)
    lleft.merge(right)
    self.node = lleft.node
    return res

  def insert(self, indx: int, key):
    node = Node(key)
    if self.node is None:
      self.node = node
      return
    if indx >= self.__len__():
      self._set_kth_elm_splay(self.__len__()-1)
      node.left = self.node
      self.node = node
    else:
      if indx < 0:
        indx += self.__len__()
      self._set_kth_elm_splay(indx)
      if self.node.left is not None:
        node.left = self.node.left
        self.node.left = None
        self._update(self.node)
      node.right = self.node
      self.node = node
    self._update(self.node)

  def append(self, key):
    self.insert(self.__len__(), key)

  def appendleft(self, key):
    self.insert(0, key)

  def popleft(self):
    return self.pop(0)

  def pop(self, indx: int =-1):
    if indx < 0:
      indx += self.__len__()
    self._set_kth_elm_splay(indx)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_max_splay(self.node.left)
      node.right = self._get_max_splay(self.node.right)
      self.node = node
    self._update(self.node)
    return res

  def copy(self):
    return SplayTree(self)

  def __setitem__(self, indx: int, key):
    self._set_kth_elm_splay(indx)
    self.node.key = key
    self._update(self.node)

  def __getitem__(self, item):
    if type(item) is int:
      self._set_kth_elm_splay(item)
      return self.node.key
    elif type(item) is slice:
      s = self.copy()
      if item.step is not None:
        s = SplayTree(list(s)[item])
      else:
        start = item.start if item.start is not None else 0
        stop  = item.stop if item.stop is not None else s.__len__()
        left, right = s.split(stop)
        lleft, s = left.split(start)
      return s
    raise KeyError

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

  def __str__(self):
    return '[' + ', '.join(map(str, self)) + ']'

  def __bool__(self):
    return self.node is not None

  def __repr__(self):
    return 'SplayTree ' + str(self)


