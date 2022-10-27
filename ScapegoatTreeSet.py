import math


class Node:
  
  def __init__(self, key):
    self.key = key
    self.left = None
    self.right = None
    self.size = 1

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size}\n'
    return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'


class ScapegoatTreeSet:
 
  alpha = 0.75
  beta = math.log2(1/alpha)
 
  '''Make a new AVLTree. / O(NlogN)'''
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
 
  def __rebuild(self, node: Node) -> Node:

    def get(node):
      if node.left is not None:
        get(node.left)
      a.append(node)
      if node.right is not None:
        get(node.right)
 
    def sort(l, r):
      if l >= r:
        return None, 0
      mid = (l + r) >> 1
      root = a[mid]
      root.left, sl = sort(l, mid)
      root.right, sr = sort(mid+1, r)
      root.size = sl+sr+1
      return root, sl+sr+1

    a = []
    get(node)
    return sort(0, len(a))[0]
 
  '''add a key. / O(logN)'''
  def add(self, key) -> bool:
    if self.node is None:
      self.node = Node(key)
      return True
    node, path = self.node, []
    while node is not None:
      path.append(node)
      if key == node.key:
        return False
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    if key < path[-1].key:
      path[-1].left = Node(key)
    else:
      path[-1].right = Node(key)
    if len(path)*self.beta > math.log(self.node.size):
      node_size = 1
      while path:
        pnode = path.pop()
        pnode_size = pnode.size + 1
        if self.alpha * pnode_size < node_size:
          break
        node_size = pnode_size
      new_node = self.__rebuild(pnode)
      if not path:
        self.node = new_node
        return True
      if new_node.key < path[-1].key:
        path[-1].left = new_node
      else:
        path[-1].right = new_node
    for p in path:
      p.size += 1
    return True
 
  '''Discard a key. / O(logN)'''
  def discard(self, key) -> bool:
    di = 1
    node, path = self.node, []
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        di, node = 1, node.left
      else:
        path.append(node)
        di, node = 0, node.right
    else:
      return False
    if node.left is not None and node.right is not None:
      path.append(node)
      di, lmax = 1, node.left
      while lmax.right is not None:
        path.append(lmax)
        di, lmax = 0, lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
    for p in path:
      p.size -= 1
    return True
 
  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key):
    res, node = None, self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res, node = node.key, node.right
    return res
 
  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key):
    res, node = None, self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        node = node.left
      else:
        res, node = node.key, node.right
    return res
 
  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key):
    res, node = None, self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        res, node = node.key, node.left
      else:
        node = node.right
    return res
 
  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key):
    res, node = None, self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        res, node = node.key, node.left
      else:
        node = node.right
    return res
 
  '''Count the number of elements < key. / O(logN)'''
  def index(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key == node.key:
        if node.left is not None:
          indx += node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        indx += 1 if node.left is None else node.left.size + 1
        node = node.right
    return indx

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key == node.key:
        indx += 1 if node.left is None else node.left.size + 1
        break
      elif key < node.key:
        node = node.left
      else:
        indx += 1 if node.left is None else node.left.size + 1
        node = node.right
    return indx

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p=-1):
    if p < 0:
      p += self.__len__()
    now, di = 0, 1
    node, path = self.node, []
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t == p:
        break
      elif t < p:
        path.append(node)
        now, di, node = t+1, -1, node.right
      elif t > p:
        path.append((node))
        di, node = 1, node.left
    else:
      raise IndexError
    res = node.key
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else -1
      while lmax.right is not None:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
    for p in path:
      p.size -= 1
    return res

  '''Return and Remove min element. / O(logN)'''
  def popleft(self):
    return self.pop(0)

  def __kth_elm(self, k):
    if k < 0:
      k += self.__len__()
    now, node = 0, self.node
    while node is not None:
      t = now if node.left is None else now + node.left.size
      if t == k:
        return node.key
      elif t < k:
        now, node = t+1, node.right
      else:
        node = node.left
    raise IndexError

  def __contains__(self, x):
    node = self.node
    while node:
      if x == node.key:
        return True
      elif x < node.key:
        node = node.left
      else:
        node = node.right
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


