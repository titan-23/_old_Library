# ScapegoatTree
まがい物のScapegoatTreeです。バグがあるかもしれません。本ライブラリでは♰ユーザーすらScapegoat♰なのです。バグ報告お待ちしております。  
載る条件は、任意の他要素との比較が可能であることです。

_____
## [ScapegoatTreeSet](https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeSet.py)
重複を許さない順序付き集合です。

### ```Node```
ノードです。キー/自身の部分木のサイズ/左の子/右の子 を保持します。

### ```st = ScapegoatTreeSet(a=[])```
iterableからScapegoatTreeSetを作ります。O(NlogN)時間です。ソート済みを仮定して内部をいじるとO(N)時間です。

### ```len(st)```
要素の個数を返します。O(1)時間です。

### ```x in st / x not in st```
存在判定です。O(logN)時間です。

### ```st[x]```
x番目に小さい値(0-indexed)を返します。負の添え字に対応しています。O(logN)時間です。

### ```bool(st) / str(st) / reversed(st)```
よしなに動きます。

### ```st.add(x)```
xがなければxを追加しTrueを返します。xがあれば追加せずにFalseを返します。償却計算量O(logN)時間です。最悪計算量はO(N)時間です。

### ```st.discard(x)```
xがあれば削除しTrueを返します。xがなければ何も削除せずにFalseを返します。O(logN)時間です。

### ```st.le(x) / .lt(x) / .ge(x) / gt(x)```
x(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。いずれもO(logN)時間です。

### ```st.index(x) / .index_right(x)```
x(より小さい/以下の)要素の数を返します。O(logN)時間です。

### ```st.pop(x=-1) / .popleft()```
x番目の要素を削除し、その値を返します。```popleft()```は```pop(0)```と等価です。いずれもO(logN)時間です。  
```st.pop(x)```は、```v = st[x]; st.discard(v); return v```より高速に動作します。


____
## [ScapegoatTreeMultiSet](https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeMultiSet.py)
重複を許可する順序付き集合です。多重集合とも。バグが多そうで怖い。正直使いたくないです。以下、おきてほしい動作を書きます。SetでできることはおそらくMultiSetでもできます。

### ```Node```
フィールドが増えました。MLEで死にそう。

### ```len(st)```
重複を含めたサイズを返します。O(1)時間です。

### ```st.len_elm()```
重複を含ないときのサイズを返します。O(1)時間です。

### ```st.count(x)```
xの要素数を返します。xが存在しないときは0を返します。O(logN)時間です。

### ```st.add(x, val=1)```
xをval個追加します。valの値に依らず、償却計算量はO(logN)時間です。

### ```st.discard(x, val=1)```
xをval個削除します。valの値に依らず、O(logN)時間です。

### ```st.discard_all(x)```
xをすべて削除します。```st.discard(x, val=st.count(x))```と等価です。O(logN)時間です。

### ```st.index_keys(x) / .index_right_keys(x)```
x(より小さい/以下)の要素の数(重複無し)を返します。O(logN)時間です。

### ```st.get_key(x)```
x番目に小さいkey(0-indexed)を返します。O(logN)時間です。

### ```st.pop(x=-1) / .popleft()```
```v = st[x]; st.discard(v); return v```と等価です。別に高速ではないです。O(logN)時間です。

### ```st.keys() / .values() / .items()```
よしなにyieldします。
