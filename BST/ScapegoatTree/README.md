# ScapegoatTree
ScapegoatTreeです。バグがあるかもしれません。ScapegoatTreeSet/MultiSetでは、ユーザーがScapegoatとならないことを保証しておりません。

## ScapegoatTreeSet
重複を許さない順序付き集合です。

### Node
各ノードは、
key, Nodeを頂点をする部分木のサイズ, 左の子, 右の子
をもっています。

### st = ScapegoatTreeSet(a=[])
iterableからSortedSetを作ります。ソートがボトルネックとなり、O(NlogN)時間です。

### len(st)
O(1)時間です。

### x in st / x not in st
O(logN)時間です。

### st.__getitem__(x)
x番目に小さい値(0-indexed)を返します。O(logN)時間です。

### bool(st) / str(st) / reversed(st)
よしなに動くはずです。

### st.add(x)
償却計算量O(logN)時間です。最悪計算量はO(N)時間です。

### st.discard(x)
O(logN)時間です。

### st.le(x) / .lt(x) / .ge(x) / gt(x)
いずれもO(logN)時間です。存在しなければNoneを返します。

### st.index(x) / .index_right(x)
x(より小さい/以下)の要素の数を返します。O(logN)時間です。

### st.pop([x]) / .popleft()
x番目の要素を削除し、そのkeyを返します。xを省略すると末尾がpopされます。また、popleftはpop(0)と等価です。いずれもO(logN)時間です。
v = st[x]; st.discard(v) より高速に動作します。


## ScapegoatTreeMultiSet
重複を許可する順序付き集合です。
