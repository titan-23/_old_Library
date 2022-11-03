# SplayTree

_____
## [SplayTreeLazy](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeLazy.py)
遅延評価ができるそうな。ただのSplayTreeには無いメソッドを書きます。

### ```st = SplayTree(a, op, mapping, composition)```
遅延セグ木のアレです。時間計算量O(N)です。

### ```st.apply(l, r, f)```
区間[l, r)に関数fを適用します。時間計算量O(logN)です。


_____
## [SplayTree](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTree.py)
列を扱えるSplayTreeです。半群がのるはずです。以下の操作が償却計算量O(logN)でできます。生後3日目くらいの幼木です。よしなに。

### ```st = SplayTree(a, op=myfunc)```
列aをSplayTreeにします。O(N)です。opは2項演算する関数です。

### ```st.merge(other)```
stにotherをmergeできます。

### ```st.split(indx)```
x, y = st.split(indx)で、indx番目で左右に分けたSplayTreeをつくりx, yに代入できます。stは破壊されます。(xの長さがindx。)

### ```st.insert(indx, key)```
indxにkeyをinsesrtできます。

### ```st.append(key) / .appendleft(key)```
末尾/先頭にkeyを追加します。

### ```st.pop(indx=-1) / .popleft()```
indx番目/先頭を削除しその値を返します。

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
セグ木的なアレです。区間[l, r)にopを適用した結果を返します。

_____
## [SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
setとしてのSplayTreeです。未完成です。よしなに。
