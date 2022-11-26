最終更新：2022/11/26

・MultiSetをアップロードしました。

_____
# [LazySplayTree](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/LazySplayTree.py)
遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。[SplayTree.py](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTree.py)でできる操作に加えて以下の操作がができます。  
※恒等写像はいりません(内部で恒等写像をNoneとして場合分けしています)。

### ```st = LazySplayTree(a, op, mapping, composition)```
列aからLazySplayTreeを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。

### ```st.reverse(l, r)```
区間[l, r)を反転します。reverse()メソッドを一度でも使用するならopには可換性が求められます(可換性がない場合、嘘の動作をします)。時間計算量(償却)O(logN)です。

### ```st.apply(l, r, f)```
区間[l, r)にfを適用します。時間計算量(償却)O(logN)です。

### ```st.all_apply(f)```
区間[0, N)にfを適用します。時間計算量O(1)です。

_____
# [SplayTree](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTree.py)
列を扱えるSplayTreeです。半群がのるはずです。以下の操作が償却計算量O(logN)でできます。

### ```st = SplayTree(a, op)```
列aからSplayTreeを構築します。O(N)です。

### ```st.merge(other)```
stにotherをmergeできます。

### ```st.split(indx)```
x, y = st.split(indx)で、indx番目で左右に分けたSplayTreeをつくりx, yに代入できます。stは破壊されます。(xの長さがindx。)

### ```st.insert(indx, key)```
indxにkeyをinsesrtできます。

### ```st.append(key) / .appendleft(key)```
末尾/先頭にkeyを追加します。st.insert(len(st), key)/st.insert(0, key)より効率が良いかもしれません。

### ```st.pop(indx=-1) / .popleft()```
indx番目/先頭を削除しその値を返します。st.pop(len(st))/st.pop(0)より効率が良いかもしれません。

### ```st[indx]```
indx番目を取得できます。

### ```st[start:stop]```
スライスします。splitです。

### ```st[start:stop:step]```
スライスします。O(N)です。

### ```st[indx] = key```
setitemできます。

### ```st.copy()```
copyできます。O(N)です。

### ```st.prod(l, r)```
区間[l, r)にopを適用した結果を返します。単位元を取得していないので、l < rが必要です。

### ```st.show(sep=' ')```
昇順にprintします。内部でsys.setrecursionlimit(len(self))をしているので安心です。O(N)です。

### ```st.to_l()```
リストに変換しま。内部でsys.setrecursionlimit(len(self))をしているので安心です。O(N)です。

_____
# [SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
集合としてのSplayTreeです。全機能をverifyしたわけではないのでコンテスト中の利用は控えると吉です。計算量を明示していないものは、償却計算量O(logN)です。

### ```st = SplayTreeSet(a=[])```
iterableからSplayTreeSetを作ります。O(NlogN)時間です。ソート済みを仮定して内部をいじるとO(N)時間です。

### ```len(st)```
要素の個数を返します。O(1)時間です。

### ```x in st / x not in st```
存在判定です。

### ```st[k]```
k番目に小さい値(0-indexed)を返します。負の添え字に対応しています。

### ```bool(st) / str(st) / reversed(st)```
よしなに動きます。

### ```st.add(x)```
xがなければxを追加しTrueを返します。xがあれば追加せずにFalseを返します。

### ```st.discard(x)```
xがあれば削除しTrueを返します。xがなければ何も削除せずにFalseを返します。

### ```st.le(x) / .lt(x) / .ge(x) / gt(x)```
x(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### ```st.index(x) / .index_right(x)```
x(より小さい/以下の)要素の数を返します。

### ```st.pop(k=-1) / .popleft()```
k番目の要素を削除し、その値を返します。   

### ```st.show(sep=' ')```
昇順にprintします。内部でsys.setrecursionlimit(len(self))をしているので安心です。

_____
# [SplayTreeMultiSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeMultiSet.py)
多重集合としてのSplayTreeです。
