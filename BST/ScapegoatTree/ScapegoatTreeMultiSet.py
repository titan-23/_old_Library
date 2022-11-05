# https://github.com/titanium-22/Library/edit/main/BST/ScapegoatTree/ScapegoatTreeMultiSet.py


import math


class Node:
  
  def __init__(self, key, val):
    self.key = key
    self.val = val
    self.left = None
    self.right = None
    self.size = 1
    self.valsize = val

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.val, self.size, self.valsize}\n'
    return f'key:{self.key, self.val, self.size, self.valsize},\n left:{self.left},\n right:{self.right}\n'


class ScapegoatTreeMultiSet:
 
  alpha = 0.75
  beta = math.log2(1/alpha)
 
  '''Make a new ScapegoatTreeMultiSet. / O(NlogN)'''
  def __init__(self, a=[]) -> None:
    if a:
      aa = sorted(a)
      a = self.__rle(aa)
    self.node = self.__build(a)

  def __rle(self, li: list) -> list:
    n = len(li)
    if n == 0:
      return []
    now = li[0]
    ret = [[now, 1]]
    for i in li[1:]:
      if i == now:
        ret[-1][1] += 1
        continue
      ret.append([i, 1])
      now = i
    return ret
 
  def __build(self, a: list) -> Node:
    def sort(l, r):
      if l >= r:
        return None, 0, 0
      mid = (l + r) >> 1
      root = Node(a[mid][0], a[mid][1])
      root.left, sl, vl = sort(l, mid)
      root.right, sr, vr = sort(mid+1, r)
      root.size = sl+sr+1
      root.valsize = vl+vr+a[mid][1]
      return root, root.size, root.valsize
    return sort(0, len(a))[0]
 
  def __rebuild(self, node: Node) -> Node:
    a = []
    def get(node):
      if node.left is not None:
        get(node.left)
      a.append(node)
      if node.right is not None:
        get(node.right)
 
    def sort(l, r):
      if l >= r:
        return None, 0, 0
      mid = (l + r) >> 1
      root = a[mid]
      root.left, sl, vl = sort(l, mid)
      root.right, sr, vr = sort(mid+1, r)
      root.size = sl+sr+1
      root.valsize = vl+vr+root.val
      return root, root.size, root.valsize
    get(node)
    return sort(0, len(a))[0]
 
  '''add a key. / O(logN)'''
  def add(self, key, val=1) -> None:
    if self.node is None:
      self.node = Node(key, val)
      return
    node, path = self.node, []
    while node is not None:
      path.append(node)
      if key == node.key:
        node.val += val
        for p in path:
          p.valsize += val
        return        
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    if key < path[-1].key:
      path[-1].left = Node(key, val)
    else:
      path[-1].right = Node(key, val)
    if len(path)*self.beta > math.log(self.__len_tree()):
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
        return
      if new_node.key < path[-1].key:
        path[-1].left = new_node
      else:
        path[-1].right = new_node
    for p in path:
      p.size += 1
      p.valsize += val
    return
 
  def __discard(self, key) -> bool:
    '''Discard node of key from self. / O(logN)'''
    path, node = [], self.node
    di, cnt = 1, 0
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        node, di = node.left, 1
      else:
        path.append(node)
        node, di = node.right,-1
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else -1
      while lmax.right is not None:
        cnt += 1
        path.append(lmax)
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
      return True
    for _ in range(cnt):
      p = path.pop()
      p.size -= 1
      p.valsize -= lmax_val
    for p in path:
      p.size -= 1
      p.valsize -= 1
    return True

  '''Discard key. / O(logN)'''
  def discard(self, key, val=1) -> bool:
    assert val >= 0
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
    if val > node.val:
      val = node.val - 1
      if val > 0:
        node.val -= val
        while path:
          path.pop().valsize -= val
    if node.val == 1:
      self.__discard(key)
    else:
      node.val -= val
      while path:
        path.pop().valsize -= val
    return True

  def count(self, key) -> int:
    node = self.node
    while node:
      if key < node.key:
        node = node.left
      elif key > node.key:
        node = node.right
      else:
        return node.val
    return 0

  def discard_all(self, key) -> None:
    self.discard(key, self.count(key))

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
          indx += node.left.valsize
        break
      elif key < node.key:
        node = node.left
      else:
        indx += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return indx

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key == node.key:
        indx += node.val if node.left is None else node.left.valsize + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        indx += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return indx

  '''Count the number of keys < key. / O(logN)'''
  def index_keys(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key == node.key:
        if node.left is not None:
          indx += node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        indx += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return indx

  '''Count the number of keys <= key. / O(logN)'''
  def index_right_keys(self, key) -> int:
    indx, node = 0, self.node
    while node:
      if key == node.key:
        indx += node.val if node.left is None else node.left.size + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        indx += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return indx

  '''Return kth elm (key). / O(logN)'''
  def get_keys(self, k):
    return self.__kth_elm_tree(k)[0]

  def pop(self, p=-1):
    '''Return and Remove max element or a[p]. / O(logN)'''
    if p < 0:
      p += self.__len__()
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

  def get_key(self, k):
    return self.__kth_elm_tree(k)[0]

  def show(self, sep=' '):
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      for _ in range(node.val):
        print(node.key, end=sep)
      if node.right is not None:
        rec(node.right)
    if self.node is not None:
      rec(self.node)

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

  def show_items(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __str__(self):
    return '{' + ', '.join(map(lambda x: ', '.join([str(x[0])]*x[1]), self.items())) + '}'

  def len_elm(self):
    return self.__len_tree()


