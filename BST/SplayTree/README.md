# SplayTree

_____
## [SplayTree](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTree.py)
列を扱えるSplayTreeです。以下の操作が償却計算量？O(logN)でできます。生後3日目くらいの幼木です。よしなに。

### ```st = SplayTree(a, op=myfunc)```
列aをSplayTreeにします。O(N)です。opは2項演算する関数です。

### ```st.merge(other)```
stにotherをmergeできます。

### ```st.split(indx)```
x, y = st.split(indx)で、indx番目で左右に分けたSplayTreeをつくりx, yに代入できます。stは破壊されます。indx番目がどっちに行くかくは忘れました。

### ```st.insert(indx, key)```
indxにkeyをinsesrtできます。

### ```st.pop(indx)```
indx番目を削除しその値を返します。

### ```st[indx]```
indx番目を取得できます。

### ```st[indx] = key```
setitemできます。

### ```st.prod(l, r)```
セグ木的なアレです。区間[l, r)にopを適用した結果を返します。opの2項演算は交換法則が成り立ってないと厳しそう。

_____
## [SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
setとしてのSplayTreeです。未完成です。よしなに。
