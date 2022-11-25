# https://github.com/titanium-22/Library/blob/main/BST/AVLTree/LazyAVLTree.py
class Node:

  def __init__(self, key):
    self.key = key
    self.data = key
    self.left = None
    self.right = None
    self.lazy = None
    self.rev = 0
    self.height = 1
    self.size = 1

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.height, self.size, self.data, self.lazy, self.rev}\n'
    return f'key:{self.key, self.height, self.size, self.data, self.lazy, self.rev},\n left:{self.left},\n right:{self.right}\n'


class LazyAVLTree:
  '''遅延伝搬反転可能AVLTree

  '''

  def __init__(self, _a=[], op=lambda x,y:None, mapping=None, composition=None, node=None):
    self.node = node
    self.op = op
    self.mapping = mapping
    self.composition = composition
    if _a:
      self._build(list(_a))

  def _build(self, a: list) -> None:
    def sort(l, r):
      if l == r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left = sort(l, mid)
      node.right = sort(mid+1, r)
      self._update(node)
      return node
    self.node = sort(0, len(a))

  def _propagate(self, node: Node) -> None:
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
    if node.left is not None:
      node.size = 1 + node.left.size
      node.data = self.op(node.left.data, node.key)
      node.height = node.left.height
    else:
      node.size = 1
      node.data = node.key
      node.height = 0
    if node.right is not None:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)
      if node.height < node.right.height:
        node.height = node.right.height
    node.height += 1

  def _get_balance(self, node):
    return (0 if node.right is None else -node.right.height) if node.left is None else (node.left.height if node.right is None else node.left.height-node.right.height)

  def _balance_left(self, node: Node) -> Node:
    # left is large
    self._propagate(node.left)
    if node.left.left is None or node.left.left.height+2 == node.left.height:
      u = node.left.right
      self._propagate(u)
      node.left.right = u.left
      u.left = node.left
      node.left = u.right
      u.right = node
      self._update(u.left)
    else:
      u = node.left
      node.left = u.right
      u.right = node
    self._update(u.right)
    self._update(u)
    return u

  def _balance_right(self, node: Node) -> Node:
    # right is large
    self._propagate(node.right)
    if node.right.right is None or node.right.right.height+2 == node.right.height:
      u = node.right.left
      self._propagate(u)
      node.right.left = u.right
      u.right = node.right
      node.right = u.left
      u.left = node
      self._update(u.right)
    else:
      u = node.right
      node.right = u.left
      u.left = node
    self._update(u.left)
    self._update(u)
    return u

  def _merge_with_root(self, l: Node, root: Node, r: Node) -> Node:
    diff = (0 if r is None else -r.height) if l is None else (l.height if r is None else l.height-r.height) 
    if diff > 1:
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      if -l.right.height if l.left is None else l.left.height-l.right.height == -2:
        return self._balance_right(l)
      return l
    elif diff < -1:
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      if r.left.height if r.right is None else r.left.height-r.right.height == 2:
        return self._balance_left(r)
      return r
    else:
      root.left = l
      root.right = r
      self._update(root)
      return root

  def _merge_fast_l(self, node, r):
    path, root = [], node
    rh = r.height
    self._propagate(node)
    while node.right is not None:
      path.append(node)
      node = node.right
      self._propagate(node)
    path.append(node.left)
    flag, root = True, node
    root.right = r
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].right = None
        self._update(path[-1])
        continue
      b = self._get_balance(node)
      path[-1].right = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
      if flag and rh <= path[-1].right.height:
        flag = False
        root.left = path[-1].right
        self._update(root)
        b = -rh if root.left is None else root.left.height-rh
        path[-1].right = self._balance_left(root) if b == 2 else self._balance_right(root) if b == -2 else root
      self._update(path[-1])
    node = path[0]
    if node is not None:
      self._update(node)
      b = self._get_balance(node)
      node = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
    if flag:
      root.left = node
      self._update(root)
      b = -rh if root.left is None else root.left.height-rh
      node = self._balance_left(root) if b == 2 else self._balance_right(root) if b == -2 else root
    return node

  def _merge_fast_r(self, l, node):
    path, root = [], node
    lh = l.height
    self._propagate(node)
    while node.left is not None:
      path.append(node)
      node = node.left
      self._propagate(node)
    path.append(node.right)
    flag, root = True, node
    root.left = l
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].left = None
        self._update(path[-1])
        continue
      b = self._get_balance(node)
      path[-1].left = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
      if flag and lh <= path[-1].left.height:
        flag = False
        root.right = path[-1].left
        self._update(root)
        b = lh if root.right is None else lh-root.right.height
        path[-1].left = self._balance_left(root) if b == 2 else self._balance_right(root) if b == -2 else root
      self._update(path[-1])
    node = path[0]
    if node is not None:
      self._update(node)
      b = self._get_balance(node)
      node = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
    if flag:
      root.right = node
      self._update(root)
      b = lh if root.right is None else lh-root.right.height
      node = self._balance_left(root) if b == 2 else self._balance_right(root) if b == -2 else root
    return node

  def _merge_node(self, l: Node, r: Node) -> Node:
    if l is None: return r
    if r is None: return l
    l, tmp = self._pop_max(l)
    return self._merge_with_root(l, tmp, r)
    # return self._merge_fast_l(l, r) if l.height > r.height else self._merge_fast_r(l, r)

  def merge(self, other) -> None:
    self.node = self._merge_node(self.node, other.node)

  def _pop_max(self, node) -> tuple:
    self._propagate(node)
    path = []
    mx = node
    while node.right is not None:
      path.append(node)
      mx = node.right
      node = node.right
      self._propagate(node)
    path.append(node.left)
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].right = None
        self._update(path[-1])
        continue
      b = self._get_balance(node)
      path[-1].right = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
      self._update(path[-1])
    if path[0] is not None:
      b = self._get_balance(path[0])
      path[0] = self._balance_left(path[0]) if b == 2 else self._balance_right(path[0]) if b == -2 else path[0]
    mx.left = None
    self._update(mx)
    return path[0], mx

  def _split_node(self, node: Node, p: int) -> tuple:
    if node is None: return None, None
    self._propagate(node)
    tmp = p if node.left is None else p-node.left.size
    if tmp == 0:
      return node.left, self._merge_with_root(None, node, node.right)
    elif tmp < 0:
      s, t = self._split_node(node.left, p)
      return s, self._merge_with_root(t, node, node.right)
    else:
      s, t = self._split_node(node.right, tmp-1)
      return self._merge_with_root(node.left, node, s), t

  def split(self, p: int) -> tuple:
    l, r = self._split_node(self.node, p)
    return LazyAVLTree([], self.op, self.mapping, self.composition, l), LazyAVLTree([], self.op, self.mapping, self.composition, r)

  def insert(self, i: int, key):
    s, t = self._split_node(self.node, i)
    self.node = self._merge_with_root(s, Node(key), t)

  def pop(self, i):
    s, t = self._split_node(self.node, i+1)
    s, tmp = self._pop_max(s)
    self.node = self._merge_node(s, t)
    return tmp.key

  def apply(self, l: int, r: int, f):
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = f if s.lazy is None else self.composition(f, s.lazy)
    self.node = self._merge_node(self._merge_node(r, s), t)

  def reverse(self, l: int, r: int):
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.rev ^= 1
    self.node = self._merge_node(self._merge_node(r, s), t)

  def prod(self, l: int, r: int):
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    res = s.data
    self.node = self._merge_node(self._merge_node(r, s), t)
    return res

  def _kth_elm(self, k):
    if k < 0:
      k += self.__len__()
    now, node = 0, self.node
    while node is not None:
      self._propagate(node)
      t = now if node.left is None else now + node.left.size
      if t < k:
        now, node = t+1, node.right
      elif t > k:
        node = node.left
      else:
        return node.key
    raise IndexError(f'k={k}, len={self.__len__()}')

  def to_l(self):
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    a = []
    if self.node is not None:
      rec(a)
    return a

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == len(self):
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self.__getitem__(-i-1)

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
