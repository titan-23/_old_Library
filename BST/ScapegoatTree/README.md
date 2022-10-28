# ScapegoatTree

## ScapegoatTreeSet

### st = ScapegoatTreeSet(a=[])
iterable から SortedSet を作ります。O(NlogN)時間です。

### len(st)

### x in st / x not in st

### st.__getitem__(x)

### bool(st) / str(st) / reversed(st)

### st.add(x)

### st.discard(x)

### st.le(x) / .lt(x) / .ge(x) / gt(x)

### st.index(x) / .index_right(x)

### st.pop([x]) / .popleft()
x番目の要素を削除し、そのkeyを返します。xを省略すると末尾がpopされます。また、popleftはpop(0)と等価です。\n
v = st[x]; st.discard(v) より高速に動作します。

