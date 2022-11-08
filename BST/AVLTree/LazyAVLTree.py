# https://github.com/titanium-22/Library/blob/main/BST/AVLTree/LazyAVLTree.py


class Node:

  def __init__(self, key):
    self.key = self.data = key
    self.left = self.right = self.lazy = None
    self.height = self.rev = 0
    self.size = 1

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size, self.data, self.lazy, self.rev}\n'
    return f'key:{self.key, self.size, self.data, self.lazy, self.rev},\n left:{self.left},\n right:{self.right}\n'


class LazyAVLTree:
  '''遅延伝搬反転可能AVLTree

  '''

  def __init__(self, _a=[], op=lambda x,y:None, mapping=None, composition=None, node=None):
    self.node = node
    self.op = op
    self.mapping = mapping
    self.composition = composition
    if _a:
      self.node = self._build(list(_a))

  def _build(self, a: list) -> None:
    def sort(l, r):
      if l == r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left, node.right = sort(l, mid), sort(mid+1, r)
      self._update(node)
      return node
    return sort(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node is None: return
    if node.rev:
      node.left, node.right = node.right, node.left
      if node.left is not None:
        node.left.rev ^= 1
      if node.right is not None:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy is not None:
      lazy = node.lazy
      if node.left is not None:
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = lazy if node.left.lazy is None else self.composition(lazy, node.left.lazy)
      if node.right is not None:
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.lazy = lazy if node.right.lazy is None else self.composition(lazy, node.right.lazy)
      node.lazy = None

  def _update(self, node: Node) -> None:
    if node is None: return
    node.size = 1
    node.data = node.key
    node.height = 0
    if node.left is not None:
      node.size += node.left.size
      node.data = self.op(node.left.data, node.data)
      node.height = node.left.height
    if node.right is not None:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)
      if node.height < node.right.height:
        node.height = node.right.height
    node.height += 1

  def _balance(self, node: Node) -> Node:
    if node is None: return None

    def rotate_right(node: Node) -> Node:
      u = node.left
      self._propagate(u)
      node.left = u.right
      u.right = node
      return u

    def rotate_left(node: Node) -> Node:
      u = node.right
      self._propagate(u)
      node.right = u.left
      u.left = node
      return u

    balance = (0 if node.left is None else node.left.height) - (0 if node.right is None else node.right.height)
    if balance == 2:
      self._propagate(node.left)
      if (0 if node.left.left is None else node.left.left.height) - (0 if node.left.right is None else node.left.right.height) == -1:
        node.left = rotate_left(node.left)
        node = rotate_right(node)
        self._update(node.left)
      else:
        node = rotate_right(node)
      self._update(node.right)
      self._update(node)
    elif balance == -2:
      self._propagate(node.right)
      if (0 if node.right.left is None else node.right.left.height) - (0 if node.right.right is None else node.right.right.height) == 1:
        node.right = rotate_right(node.right)
        node = rotate_left(node)
        self._update(node.right)
      else:
        node = rotate_left(node)
      self._update(node.left)
      self._update(node)
    return node

  def _merge_with_root(self, l: Node, root: Node, r: Node) -> Node:
    diff = (0 if l is None else l.height) - (0 if r is None else r.height)
    if -1 <= diff and diff <= 1:
      self._propagate(root)
      root.left = l
      root.right = r
      self._update(root)
      return root
    elif diff > 0:
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      return self._balance(l)
    else:
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      return self._balance(r)

  def _pop_max(self, node) -> tuple:
    if self.node is None: return None, None
    self._propagate(node)
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
      self._propagate(node)
    mx = node
    if path:
      path[-1].right = node.left
      path.append(node.left)
      while path:
        node = path.pop()
        if path:
          path[-1].right = self._balance(node)
          self._update(path[-1])
    else:
      node = node.left
    mx.left = None
    self._update(mx)
    return node, mx

  def _merge_node(self, l: Node, r: Node) -> Node:
    if l is None: return r
    # if r is None: return l
    l, tmp = self._pop_max(l)
    return self._merge_with_root(l, tmp, r)

  def merge(self, r: Node) -> None:
    self.node = self._merge_node(self.node, r)

  def _split_node(self, node: Node, p: int) -> tuple:
    def _split(node, p: int) -> tuple:
      if node is None:
        return None, None
      self._propagate(node)
      l = node.left
      r = node.right
      node.left = None
      node.right = None
      lsize = 0 if l is None else l.size
      if p < lsize:
        s, t = _split(l, p)
        return s, self._merge_with_root(t, node, r)
      elif p > lsize:
        s, t = _split(r, p-lsize-1)
        return self._merge_with_root(l, node, s), t
      else:
        return l, self._merge_with_root(None, node, r)
    return _split(node, p)

  def split(self, p: int) -> tuple:
    l, r = self._split_node(self.node, p)
    return LazyAVLTree([], self.op, self.mapping, self.composition, l), LazyAVLTree([], self.op, self.mapping, self.composition, r)

  def insert(self, i: int, key):
    s, t = self._split_node(self.node, i)
    self.node = self._merge_with_root(s, Node(key), t)

  def pop(self, i):
    s, t = self._split_node(self.node, i+1)
    self.node, tmp = self._pop_max(s)
    self.merge(t)
    return tmp.key

  def apply(self, l: int, r: int, f):
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = f if s.lazy is None else self.composition(f, s.lazy)
    r = self._merge_node(r, s)
    self.node = self._merge_node(r, t)

  def reverse(self, l: int, r: int):
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.rev ^= 1
    r = self._merge_node(r, s)
    self.node = self._merge_node(r, t)

  def prod(self, l: int, r: int):
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    res = s.data
    r = self._merge_node(r, s)
    self.node = self._merge_node(r, t)
    # self.node = self._merge_node(self._merge_node(r, s), t) ???
    return res

  def _kth_elm(self, k):
    if k < 0:
      k += self.__len__()
    now = 0
    node = self.node
    while node is not None:
      self._propagate(node)
      t = now if node.left is None else now + node.left.size
      if t < k:
        now = t + 1
        node = node.right
      elif t > k:
        node = node.left
      else:
        return node.key
    raise IndexError(f'k={k}, len={self.__len__()}')

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __getitem__(self, k):
    return self._kth_elm(k)

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(len(self))])) + ']'

  def __repr__(self):
    return 'LazyAVLTree ' + str(self)


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

