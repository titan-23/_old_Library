import sys
from array import array
from typing import Generic, List, TypeVar, Callable, Iterable, Optional, Union
T = TypeVar("T")
F = TypeVar("F")

class LinkCutTree(Generic[T, F]):

  # path applyをするにはコメントアウトを外すこと

  def __init__(self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None):
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e

    self.key:   List[T] = [e for _ in range(n_or_a)] if isinstance(n_or_a, int) else [e for e in n_or_a]
    self.n = len(self.key)
    self.key.append(self.e)
    self.data:  List[T] = self.key[:]
    self.rdata: List[T] = self.key[:]
    # self.lazy:  List[Optional[F]] = [None] * (self.n+1)
    
    # self.par  : List[int] = [self.n] * (self.n+1)
    # self.left : List[int] = [self.n] * (self.n+1)
    # self.right: List[int] = [self.n] * (self.n+1)
    # self.size : List[int] = [1] * (self.n+1)
    # self.rev  : List[int] = [0] * (self.n+1)
    _n = [self.n] * (self.n+1)
    self.par  : array[int] = array('I', _n)
    self.left : array[int] = array('I', _n)
    self.right: array[int] = array('I', _n)
    self.size : array[int] = array('I', [1] * (self.n+1))
    self.rev  : array[int] = array('I', bytes(4*(self.n+1)))
    self.size[self.n] = 0

  def _is_root(self, node: int) -> bool:
    return (self.par[node] == self.n) or not (self.left[self.par[node]] == node or self.right[self.par[node]] == node)

  def _propagate(self, node: int) -> None:
    # nodeの左右の子に遅延素子を伝搬する 詳しくは見れば分かる
    if node == self.n or self.rev[node] == 0: return
    rev, data, rdata = self.rev, self.data, self.rdata
    left, right = self.left, self.right
    data[node], rdata[node] = rdata[node], data[node]
    left[node], right[node] = right[node], left[node]
    if left[node] != self.n: rev[left[node]] ^= 1
    if right[node] != self.n: rev[right[node]] ^= 1
    rev[node] = 0
    return
    if self.lazy[node] is not None:
      lazy = self.lazy[node]
      if self.left[node] != self.n:
        data[left[node]] = self.mapping(lazy, data[left[node]])
        rdata[left[node]] = self.mapping(lazy, rdata[left[node]])
        self.key[left[node]] = self.mapping(lazy, self.key[left[node]])
        self.lazy[left[node]] = lazy if self.lazy[left[node]] is None else self.composition(lazy, self.lazy[left[node]])
      if self.right[node] != self.n:
        data[right[node]] = self.mapping(lazy, data[right[node]])
        rdata[right[node]] = self.mapping(lazy, rdata[right[node]])
        self.key[right[node]] = self.mapping(lazy, self.key[right[node]])
        self.lazy[right[node]] = lazy if self.lazy[right[node]] is None else self.composition(lazy, self.lazy[right[node]])
      self.lazy[node] = None

  def _update(self, node: int) -> None:
    if node == self.n: return
    ln, rn = self.left[node], self.right[node]
    self._propagate(ln)  # この処理が必要 場合分けをしてもいいが、
    self._propagate(rn)  # propagateすると遅延素子が無くなるのでうれしいかも
    self.size[node] = 1 + self.size[ln] + self.size[rn]
    self.data[node] = self.op(self.op(self.data[ln], self.key[node]), self.data[rn])
    self.rdata[node] = self.op(self.op(self.rdata[rn], self.key[node]), self.rdata[ln])

  def _update_triple(self, x: int, y: int, z: int) -> None:
    size, data, rdata = self.size, self.data, self.rdata
    key, left, right = self.key, self.left, self.right
    size[z] = size[x]
    data[z] = data[x]
    rdata[z] = rdata[x]
    lx, rx = left[x], right[x]
    ly, ry = left[y], right[y]
    self._propagate(lx)
    self._propagate(rx)
    self._propagate(ly)
    self._propagate(ry)
    data[x] = self.op(self.op(data[lx], key[x]), data[rx])
    data[y] = self.op(self.op(data[ly], key[y]), data[ry])
    rdata[x] = self.op(self.op(rdata[rx], key[x]), rdata[lx])
    rdata[y] = self.op(self.op(rdata[ry], key[y]), rdata[ly])
    size[x] = 1 + size[lx] + size[rx]
    size[y] = 1 + size[ly] + size[ry]

  def _splay(self, node: int) -> None:
    # splayを抜けた後、nodeは遅延伝播済みにするようにする
    # (splay後のnodeのleft,rightにアクセスしやすいと非常にラクなはず)
    if node == self.n: return
    if self._is_root(node):
      self._propagate(node)
      return
    left, right, par = self.left, self.right, self.par
    self._propagate(node)
    while par[par[node]] != self.n:
      pnode = par[node]
      if self._is_root(pnode): break
      gnode = par[pnode]
      self._propagate(gnode)
      self._propagate(pnode)
      self._propagate(node)
      par[node] = par[gnode]
      # いつものzig-zag4通り場合分け
      if (left[gnode] == pnode) == (left[pnode] == node):
        if left[pnode] == node:
          tmp1 = right[node]
          left[pnode] = tmp1
          right[node] = pnode
          tmp2 = right[pnode]
          left[gnode] = tmp2
          right[pnode] = gnode
        else:
          tmp1 = left[node]
          right[pnode] = tmp1
          left[node] = pnode
          tmp2 = left[pnode]
          right[gnode] = tmp2
          left[pnode] = gnode
        if tmp1 != self.n:
          par[tmp1] = pnode
        if tmp2 != self.n:
          par[tmp2] = gnode
        par[pnode] = node
        par[gnode] = pnode
      else:
        if left[pnode] == node:
          tmp1 = right[node]
          left[pnode] = tmp1
          right[node] = pnode
          tmp2 = left[node]
          right[gnode] = tmp2
          left[node] = gnode
        else:
          tmp1 = left[node]
          right[pnode] = tmp1
          left[node] = pnode
          tmp2 = right[node]
          left[gnode] = tmp2
          right[node] = gnode
        if tmp1 != self.n:
          par[tmp1] = pnode
        if tmp2 != self.n:
          par[tmp2] = gnode
        par[pnode] = node
        par[gnode] = node
      self._update(gnode)
      self._update(pnode)
      self._update(node)
      # self._update_triple(gnode, pnode, node)
      
      ggnode = par[node]
      if ggnode == self.n:
        self._propagate(node)
        return
      # 元の親の親の親との付け替え 今のnodeの親とgnodeを比較
      if left[ggnode] == gnode:
        left[ggnode] = node
      elif right[ggnode] == gnode:  # elseにしてはいけない
        right[ggnode] = node
      self._propagate(ggnode)
      self._update(ggnode)  # par[node]をpropagateするとよさそう？ホント？
      
      if self._is_root(node):
        self._propagate(node)
        return

    if self._is_root(node):
      self._propagate(node)
      return
    pnode = par[node]
    self._propagate(pnode)
    self._propagate(node)
    if left[pnode] == node:
      left[pnode] = right[node]
      if left[pnode] != self.n:
        par[left[pnode]] = pnode
      right[node] = pnode
    else:
      right[pnode] = left[node]
      if right[pnode] != self.n:
        par[right[pnode]] = pnode
      left[node] = pnode
    par[node] = par[pnode]
    par[pnode] = node
    self._update(pnode)
    self._update(node)

  def expose(self, v: int) -> None:
    ''' 「元の木」のvを含む部分木において、vをsplayする
    実装では
    ・vをsplay
    ・vのparがあれば、それは「元の木」の一部なので、par[v]の右にvを入れてwhile文継続
    など
    '''
    right, par = self.right, self.par
    while True:
      self._splay(v)
      right[v] = self.n
      self._update(v)
      if par[v] == self.n: break
      self._splay(par[v])
      right[par[v]] = v
      self._update(par[v])
    self._splay(v)
    right[v] = self.n
    self._update(v)

  def link(self, c: int, p: int) -> None:
    ''' c->pの辺を追加する / cは元の木の根でなければならない
    (元の木の根とself._is_root()はまったくの別物)
    '''
    assert not self.same(c, p)
    self.expose(c)
    self.expose(p)
    self.par[c] = p
    self.right[p] = c
    self._update(p)

  def cut(self, c: int) -> None:
    ''' cとpar[c]の間の辺を削除する / cは元の木の根であってはいけない
    '''
    self.expose(c)
    assert self.left[c] != self.n
    self.par[self.left[c]] = self.n
    self.left[c] = self.n
    self._update(c)

  def root(self, v: int) -> int:
    self.expose(v)
    self._propagate(v)
    left = self.left
    while left[v] != self.n:
      v = left[v]
      self._propagate(v)
    self._splay(v)
    return v

  def same(self, u: int, v: int) -> bool:
    ''' uとvが同じ連結成分であるかを返す
    '''
    return self.root(u) == self.root(v)

  def evert(self, v: int) -> None:
    ''' vが属するsplay木の根をvにする
    元の木に変化はないはず
    evert後、vは遅延伝播済み(何かと便利なので)
    '''
    self.expose(v)
    self.rev[v] ^= 1
    self._propagate(v)

  def prod(self, u: int, v: int) -> T:
    ''' パス[u -> v]間の総積を返す
    非可換に対応済み
    '''
    self.evert(u)
    self.expose(v)
    return self.data[v]

  def apply(self, u: int, v: int, f: F) -> None:
    # self.evert(u)
    # self.expose(v)
    # node = v
    # self.key[node] = self.mapping(f, self.key[node])
    # self.data[node] = self.mapping(f, self.data[node])
    # self.rdata[node] = self.mapping(f, self.rdata[node])
    # self.lazy[node] = f if self.lazy[node] is None else self.composition(f, self.lazy[node])
    pass

  def merge(self, u: int, v: int) -> bool:
    ''' uとvをmergeする / sameチェックは仕様
    '''
    if self.same(u, v): return False
    self.evert(u)
    self.link(u, v)
    return True

  def split(self, u: int, v: int) -> bool:
    ''' uとvをsplitする / sameチェックは仕様
    '''
    if not self.same(v, u): return False
    self.evert(u)
    self.cut(v)
    return True

  def group_count(self) -> int:
    # O(N)
    return sum(1 for e in self.par if e == self.n) - 1

  def path_kth_elm(self, s: int, t: int, k: int) -> Optional[int]:
    '''path[s -> t]のk番目を取得する
    '''
    self.evert(s)
    self.expose(t)
    if self.size[t] <= k:
      return None
    size, left, right = self.size, self.left, self.right
    while True:
      self._propagate(t)
      s = size[left[t]]
      if s == k:
        self._splay(t)
        return t
      elif s > k:
        t = left[t]
      else:
        t = right[t]
        k -= s + 1

  def __setitem__(self, k: int, v: T):
    self._splay(k)
    self.key[k] = v
    self._update(k)

  def __getitem__(self, k: int) -> T:
    self._splay(k)
    return self.key[k]

  def __str__(self):
    # 分からん
    return 'LinkCutTree()'


def op(s, t):
  return

