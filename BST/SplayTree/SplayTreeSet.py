https://github.com/titanium-22/Library/edit/main/BST/SplayTree/SplayTreeSet.py


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
    self.node = self._build(a)

  def _build(self, a: list) -> None:
    def sort(l, r):
      if l >= r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left, node.right = sort(l, mid), sort(mid+1, r)
      self._update(node)
      return node
    return sort(0, len(a))

  def _update(self, node):
    if node is None: return
    node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)

  def _splay(self, path, di) -> Node:
    # assert len(path) > 0
    while len(path) > 1:
      node, pnode = path.pop(), path.pop()
      ndi, pdi = di&1, di>>1&1
      di >>= 2
      if ndi == pdi:
        if ndi:
          tmp, node.left = node.left, node.left.right
          tmp.right, pnode.left, node.right = node, node.right, pnode
        else:
          tmp, node.right = node.right, node.right.left
          tmp.left, pnode.right, node.left = node, node.left, pnode
      else:
        if ndi:
          tmp, node.left = node.left, node.left.right
          pnode.right, tmp.right, tmp.left = tmp.left, node, pnode
        else:
          tmp, node.right = node.right, node.right.left
          pnode.left, tmp.left, tmp.right = tmp.right, node, pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      if di & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1:
      node = gnode.left
      gnode.left, node.right = node.right, gnode
      self._update(node.right)
    else:
      node = gnode.right
      gnode.right, node.left = node.left, gnode
      self._update(node.left)
    self._update(node)
    return node

  def _set_search_splay(self, key) -> None:
    node = self.node
    if node is None or node.key == key:
      return
    path, di = [], 0
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di, node = di<<1|1, node.left
      else:
        path.append(node)
        di, node = di<<1, node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)

  def _set_kth_elm_splay(self, k: int) -> None:
    now, di = 0, 0
    node, path = self.node, []
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t == k:
        if len(path) > 0:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di, node = di<<1|1, node.left
      else:
        path.append(node)
        di, node, now = di<<1, node.right, t+1
    raise IndexError

  def _get_min_splay(self, node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  '''Add a key. / O(logN)'''
  def add(self, key) -> bool:
    if self.node is None:
      self.node = Node(key)
      return True
    self._set_search_splay(key)
    if self.node.key == key:
      return False
    node = Node(key)
    if key < self.node.key:
      node.right, node.left = self.node, self.node.left
      self.node.left = None
      self._update(node.right)
    else:
      node.left, node.right = self.node, self.node.right
      self.node.right = None
      self._update(node.left)
    self.node = node
    self._update(self.node)
    return True

  '''Discard a key. / O(logN)'''
  def discard(self, key):
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
      self._update(self.node.left)
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    path, di, res = [], 0, None
    node = self.node
    if node is None: return None
    while node is not None:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        path.append(node)
        di, node = di<<1|1, node.left
      else:
        path.append(node)
        di, res, node = di<<1, node.key, node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    path, di, res = [], 0, None
    node = self.node
    if node is None: return None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di, node = di<<1|1, node.left
      else:
        path.append(node)
        di, res, node = di<<1, node.key, node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    path, di, res = [], 0, None
    node = self.node
    if node is None: return None
    while node is not None:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        path.append(node)
        di, res, node = di<<1|1, node.key, node.left
      else:
        path.append(node)
        di, node = di<<1, node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    path, di, res = [], 0, None
    node = self.node
    if node is None: return None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di, res, node = di<<1|1, node.key, node.left
      else:
        path.append(node)
        di, node = di<<1, node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key) -> int:
    self._set_search_splay(key)
    if self.node.left is None:
      res = 0
    else:
      res = self.node.left.size
    return res

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    self._set_search_splay(key)
    if self.node.left is None:
      res = 0
    else:
      res = self.node.left.size
    return res + (self.node.key == key)

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p=-1):
    if p == -1:
      node = self._get_max_splay(self.node)
      self.node = node.left
      return node.key
    if p < 0:
      p += self.__len__()
    self._set_kth_elm_splay(p)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
      self._update(self.node.left)
    return res

  '''Return and Remove min element. / O(logN)'''
  def popleft(self):
    node = self._get_min_splay(self.node)
    self.node = node.right
    return node.key

  '''Print self. / O(N)'''
  def show(self, sep=' '):
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      print(node.key, end=sep)
      if node.right is not None:
        rec(node.right)
    if self.node is not None:
      rec(self.node)

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

  def __contains__(self, key):
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __getitem__(self, indx):
    if indx < 0:
      indx += self.__len__()
    self._set_kth_elm_splay(indx)
    return self.node.key

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, [self.__getitem__(i) for i in range(self.__len__())])) + '}'

  def __repr__(self):
    return 'SplayTreeSet ' + str(self)


