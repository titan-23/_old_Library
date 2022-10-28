# ScapegoatTree
ScapegoatTreeです。バグがあるかもしれません。ScapegoatTreeSet/MultiSetでは、ユーザーがScapegoatとならないことを保証しておりません。

## ScapegoatTreeSet
重複を許さない順序付き集合です。

### Node
各ノードは、
key, Nodeを頂点をする部分木のサイズ, 左の子, 右の子
をもっています。

### st = ScapegoatTreeSet(a=[])
iterableからScapegoatTreeSetを作ります。ソートがボトルネックとなり、O(NlogN)時間です。

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
いずれもO(logN)時間です。存在しなければNoneを返します。ところで、何を返すか言っていませんね。

### st.index(x) / .index_right(x)
x(より小さい/以下)の要素の数を返します。O(logN)時間です。

### st.pop(x=-1) / .popleft()
x番目の要素を削除し、そのkeyを返します。xを省略すると末尾がpopされます。また、popleftはpop(0)と等価です。いずれもO(logN)時間です。
v = st[x]; st.discard(v) より高速に動作します。


## ScapegoatTreeMultiSet
重複を許可する順序付き集合です。バグが多そうで怖い。正直使いたくないです。以下、おきてほしい動作を書きます。SetでできることはおそらくMultiSetでもできます。

### len(st)
重複を含めたサイズを返します。O(1)時間です。

### st.len_elm()
重複を含ないときのサイズを返します。O(1)時間です。

### st.count(x)
xの要素数を返します。xが存在しないときは0を返します。O(logN)時間です。

### st.add(x, cnt=1)
xをcnt個追加します。cntを省略すると1つのみ追加されます。cntの値に依らず、償却計算量はO(logN)時間です。

### st.discard(x, cnt=1)
xをcnt個削除します。cntを省略すると1つのみ追加されます。cntの値に依らず、O(logN)時間です。

### st.discard_all(x)
xをすべて削除します。O(logN)時間です。

### st.index_keys(x) / .index_right_keys(x)
x(より小さい/以下)の要素の数(重複無し)を返します。O(logN)時間です。

### st.get_key(x)
x番目に小さいkey(0-indexed)を返します。O(logN)時間です。

### st.keys() / .values() / .items()
yieldします。